from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from tortoise.exceptions import IntegrityError
from os import path

from Repository.UserRepository import UserRepository
from Repository.LinkRepository import LinkRepository

_BASE = path.dirname(path.dirname(path.abspath(__file__)))

view_router = APIRouter(tags=["Views"])
templates = Jinja2Templates(directory=path.join(_BASE, "View"))


def _get_user(request: Request):
    return request.session.get("user")


@view_router.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(request, "index.html")


# ── Auth ──────────────────────────────────────────────────────────────────────

@view_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if _get_user(request):
        return RedirectResponse("/dashboard", status_code=302)
    return templates.TemplateResponse(request, "login.html")


@view_router.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    user = await UserRepository().getUserByEmail(email)
    if not user or user.password != password:
        return templates.TemplateResponse(
            request, "login.html", {"error": "E-mail ou senha inválidos."}
        )
    request.session["user"] = {"id": user.id, "name": user.name, "email": user.email}
    return RedirectResponse("/dashboard", status_code=302)


@view_router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    if _get_user(request):
        return RedirectResponse("/dashboard", status_code=302)
    return templates.TemplateResponse(request, "register.html")


@view_router.post("/register", response_class=HTMLResponse)
async def register_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    try:
        new_user = await UserRepository().createUser(name=name, email=email, password=password)
        request.session["user"] = {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
        }
        return RedirectResponse("/dashboard", status_code=302)
    except IntegrityError:
        return templates.TemplateResponse(
            request, "register.html", {"error": "Este e-mail já está em uso."}
        )


@view_router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)


# ── Dashboard ─────────────────────────────────────────────────────────────────

@view_router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = _get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    links = await LinkRepository().getLinksByUserId(user["id"])
    total_bad   = sum(l["bad"]   for l in links)
    total_good  = sum(l["good"]  for l in links)
    total_great = sum(l["great"] for l in links)
    total       = total_bad + total_good + total_great
    satisfaction = round(total_great / total * 100) if total else 0
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "user": user,
            "links": links,
            "stats": {
                "total_links": len(links),
                "total_responses": total,
                "satisfaction": satisfaction,
            },
        },
    )


@view_router.post("/dashboard/create")
async def create_evaluation(request: Request, name: str = Form(...)):
    user = _get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    await LinkRepository().createLink(name, user["id"])
    return RedirectResponse("/dashboard", status_code=302)


# ── Evaluation detail ─────────────────────────────────────────────────────────

@view_router.get("/evaluation/{link_id}", response_class=HTMLResponse)
async def evaluation_detail(request: Request, link_id: int):
    user = _get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    link = await LinkRepository().getLinkWithRating(link_id, user["id"])
    if not link:
        return RedirectResponse("/dashboard", status_code=302)
    base_url = str(request.base_url).rstrip("/")
    return templates.TemplateResponse(
        request,
        "evaluation.html",
        {"user": user, "link": link, "base_url": base_url},
    )


@view_router.post("/evaluation/{link_id}/rename")
async def rename_evaluation(request: Request, link_id: int, name: str = Form(...)):
    user = _get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    await LinkRepository().updateLinkName(link_id, name)
    return RedirectResponse(f"/evaluation/{link_id}", status_code=302)


@view_router.post("/evaluation/{link_id}/delete")
async def delete_evaluation(request: Request, link_id: int):
    user = _get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    await LinkRepository().deletLink(link_id)
    return RedirectResponse("/dashboard", status_code=302)


# ── Customer rating page ──────────────────────────────────────────────────────

@view_router.get("/rate/{link_id}/{rating}", response_class=HTMLResponse)
async def rate_page(request: Request, link_id: int, rating: str):
    if rating not in ("bad", "good", "great"):
        return RedirectResponse("/", status_code=302)
    await LinkRepository().updateLinkRating(link_id, rating)
    return templates.TemplateResponse(request, "rate.html", {"rating": rating})


# ── Profile ───────────────────────────────────────────────────────────────────

@view_router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    user = _get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    return templates.TemplateResponse(request, "profile.html", {"user": user})


@view_router.post("/profile/update-name")
async def update_name(request: Request, name: str = Form(...)):
    user = _get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    await UserRepository().updateUserInfo("name", name, user["id"])
    request.session["user"]["name"] = name
    return RedirectResponse("/profile?success=Nome+atualizado", status_code=302)


@view_router.post("/profile/update-password")
async def update_password(request: Request, password: str = Form(...)):
    user = _get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    await UserRepository().updateUserInfo("password", password, user["id"])
    return RedirectResponse("/profile?success=Senha+atualizada", status_code=302)


@view_router.post("/profile/delete")
async def delete_account(request: Request):
    user = _get_user(request)
    if not user:
        return RedirectResponse("/login", status_code=302)
    await UserRepository().deleteUser(user["id"])
    request.session.clear()
    return RedirectResponse("/", status_code=302)
