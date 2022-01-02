## Setup test server

1. git
    - Download project
        ```
        git clone https://nas.pdogs.ntu.im:30443/pdogs/pdogs-6/backend-entry-task/entry_task_wsa.git
        ```
2. conda env

    - open your cmd and go to the file `entry_task_wsa`
    - Create a new environment
        ```
        conda create --name my-blog python=3.8
        ```
    - Activate environment
        ```
        conda activate my-blog
        ```
    - Install dependencies
        ```
        pip install -r requirements.txt
        ```
3. install docker

    - [docker](https://www.docker.com/products/docker-desktop)
    - use cmd go to the folder
        ```
        copy docker-compose.yaml.example docker-compose.yaml
        ```
      
        ```
        docker-compose up
        ```
    
4. install dbeaver
    - [dbeaver](https://dbeaver.io/)
    - open it and press `alt + d`, choose `新建連結`, then choose `postgresql`.(我用簡體版)
      
      主機: localhost, 端口:5432
      
      數據庫: test_db 
      
      用戶名: test_user
      
      密碼:   test_password
    - press `control + alt + enter`, then copy and paste words in `schema.sql` into it, then
      `control + enter`.
5. set up environment
    ```
   copy .env.example .env
    ```
   fill out db information in `.env`
   

6. Start the server
    
    - install uvicorn
        ```
        pip install uvicorn
        ```
    - Run app
        ```
        uvicorn app:app --reload
        ```
    now you can go http://127.0.0.1:8000/docs and check the api
   
7. APIs

- output classes:
        
    - class `PostOutput`:
   
                id: int
                name: str
                content: str
                time: datetime
        
    - class `CommentOutput`:
         
                id: int
                post_id: int
                name: str
                message: str
                time: datetime

   
- browse_post()
      
      input: none
      
      output: sequence of class PostOutput
   

- read_post(`post_id: int`)
      
      input: an interger "id"
    
      output: class PostOutput

- add_post(`name: str`, `content: str`)
      
      input: string "name" and "content"
  
      output: an integer represents post's "id"
    
- delete_post(`post_id: int`)
   
      input: an interger "id"

      output: "post 'id' is deleted."

- edit_post(`post_id: int`, `name: str`, `content: str`)

      input: an interger "id" 
             a string "name" <optional>
             a string "content" <optional>

      output: "post 'id' has been edited."

- browse_comment(`post_id: int`)

      input: an interger "id"

      output: sequence of class CommentOutput

- add_comment(`post_id: int`, `name: str`, `message: str`)
   
      input: an interger 'post_id' represents which post the comment is on.
             a string "name"
             a string "message"

      output: an interger represent comment's id.