I did the extension.
The only issue is that I am not sure how to get ON DELETE CASCADE working with sqlalchemy,
so you wouldn't be able to delete an element that contains a tag.

Also, all of the test cases are passed, but for some reason, the frontend only loads on the initial /boards page.
After clicking on a board, nothing shows up even though /kanban/boards/{board_id} contains the appropriate JSON
information. 
