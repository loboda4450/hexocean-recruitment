# HexOcean recruitment task

### Setup
- To run app just exec `run.sh`, it will:
  - create `venv` 
  - install dependencies inside `venv`
  - make migrations
  - migrate
  - build containter using `docker-compose`
- If you want to explore browsable api enter in browser
  - `http://localhost:8000`
- `curl` examples are listed below
- there are prepared users:
  - superuser `hexocean:hexoceanpassword#1!`
  - user with enterprise tier `example:examplepassword#1!`
- there is `Custom tier` with Enterprise + 300px permission


### Informations
- It took me about 25 hours to code it. I faced some problems probably distro-based (thanks Arch), that did not happen on my private server running Ubuntu - realized too late.
- Thumbnail sizes are based on permissions, so if you want to add arbitrary thumbnail size you have to add new permission with `codename` of desired size (integer)
- To create arbitrary tiers you have to create new group with desired (probably newly created) permissions. Adding, removing and viewing images permissions are added by default.
- After you obtain temporary url you have to fill a parameter `timeout` at the end of url with desired link expiration seconds (e.g 300, 500)


### Example curls
It is easier to use links returned by API, because it uses `uuid4` namespace, and I believe it's hardly guessable what your uploaded images names are :D
- Getting user images (tier-based links):
  - `curl -X GET http://host:8000/images/ -u "username:password"`
- Posting images:
  - `curl -X POST -F "image_fullres=@path/to/image" http://host:8000/images/ -u "username:password"`
- Deleting images:
  - `curl -X DELETE http://host:8000/images/<int:pk>/ -u "username:password"`
- Creating permission:
  - `curl -X POST -F "codename=<desired thumbnail height><int>" -F "name=Can get <desired thumbnail height>px in height image" http://host:8000/permissions/ -u "username:password"`
- Creating tiers:
  - `curl -X POST -F "name=<desired tier name>" -F "permission=<int:pk>" -F "permission=<int:pk>" http://host:8000/groups/ -u "username:password"`

### Requirements completed:
- [x] docker-compose
- [ ] live preview
- [x] tests
- [x] Upload images via HTTP request
  - [x] Validate image type
  - [x] Save with custom id
  - [x] Generate binary from image
- [x] Users able to list their images
- [x] Default tier "Basic"
  - [x] Thumbnail 200px
- [x] Default tier "Premium"
  - [x] Thumbnail 200px
  - [x] Thumbnail 400px
- [x] Default tier "Enterprise"
  - [x] Thumbnail 200px
  - [x] Thumbnail 400px
  - [x] Fully-sized image
  - [x] Expiring links (from 300 to 30000 seconds)
- [x] Admins able to create arbitrary tiers
  - [x] Arbitrary thumbnail size
  - [x] Presence of the full-sized image
  - [x] Ability of generating expiring links