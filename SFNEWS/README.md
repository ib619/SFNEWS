# D5.6: D5.6_AUTH
* All pages are accesible through the UI:
    1. Each page has dropdown where All Posts, Post Search and My Account are available through links
    2. In My Account, the user can log out, become an author, or create a post if is an author
* Templates for some foreign views were overriden:
    1. The 403 Forbidden Page
    2. Login, Signup and Password Reset pages from django-allauth
* Known issues:
    1. If user signs up through a provider like google, it is not automatically added to common group
    2. If user signs up through the sign up page, it is succesfully added to common group
    3. This issue can be resolved through overriding the google OAuth form, but I was not able to do it. This does not affect the work of the web application significantly