# HexOcean recruitment task

### Setup
- Thumbnail sizes are based on permissions, so if you want to add arbitrary thumbnail size you have to add new permission with `codename` of desired size (integer)
- To create arbitrary tiers you have to create new group with desired (probably newly created) permissions. Adding, removing and viewing permissions are added by default.

To create user you do not have to access  
It is easier to use links returned by API, because it uses `uuid4` namespace, and I believe it's hardly guessable what your uploaded images names are :D
- Getting user images (tier-based links):
  - `curl -X GET http://host:8000/images/ -u "username:password"`
- Posting images:
  - `curl -X POST -F "image_fullres=@path/to/image" http://host:8000/images/ -u "username:password"`
- Deleting images:
  - `curl -X DELETE http://host:8000/images/<pk>/ -u "username:password"`


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