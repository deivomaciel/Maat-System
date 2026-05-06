MaatS

Functionals Requirementes:
- The user should be able to create a new link to rate their service
<!-- - The user should be able to add many rate options as they want -->
- The user should be able to delete their links
- The user should be able to view their links metrics
- The user should be albe to create a link to notfy wen the e-mail was opened

Entitys:
- User - id, name, email, password
- link - id, id_user, name, token
- rated_link - id, id_link, bad, good, great