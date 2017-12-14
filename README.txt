--------------------------------------
- WebTodo: A simple todo application -
--------------------------------------

What it is:
  WebTodo is a simple web application that allows users to create
and manage simple todo lists.

What it does:
  Users can create an account and create/manage simple todo lists.
Once logged in, users can add, edit, mark complete/incomplete, and delete
todo list items. Todo list items have a title (required) and note (optional).

Models:
  USER
    - id: primary
    - username: unique
    - password: hashed
    - (email)

  LIST_ITEMS
    - id: primary
    - ownerid: foreign key
    - title: String (140)
    - note: String
    - completed: Boolean (true if created)
    - (date created: DateTime)

Views:
  homepage
    - Logged out: shows welcome, links to login/signup forms
    - Logged in: shows todo list
        - LINKS: [add_item, edit_item, mark_item_(in)complete, delete item,
                  edit_profile, sign_out]

  sign up
    - Displays a form with username, email, password, password validation fields
    - LINKS: [sign_up, login, home]

  log in
    - Displays a form with username and password fields
    - LINKS: [login, sign_up, home]

  add item (login_required)
    - Displays form with title and note fields
    - LINKS: [submit, cancel, home, sign_out, edit_profile]

  edit item
    - Displays form with title and note fields pre-filled with list item information
    - LINKS: [submit, cancel, home, sign_out, edit_profile]

  mark item (in)complete
    - Not a view; URL endpoint that will mark a list item complete or incomplete (item id given in url)

  delete item
    - Displays a warning about permanent deletion, etc.
    - Displays form with a big red delete button and cancel button
    - LINKS: [DELETE, cancel, home, sign_out, edit_profile]

  edit profile
    - Displays current username and email, button to reset password
    - username and email fields are editable (hidden form)
    - reset password displays a hidden form asking for new password and confirmation
    - LINKS: [home, sign_up] (all above editable info done via hidden form)
