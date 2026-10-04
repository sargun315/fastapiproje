from fastapi import FastAPI, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from auth import create_token, verify_token
from database import engine,SessionLocal
import models,schemas

models.Base.metadata.create_all(bind=engine)

app=FastAPI()

#db Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   

#login api
@app.post("/login")
def login():
    return{
        "access_ token": create_token({"user":"admin"}),
        "token_type": "bearer"
    }

#home
@app.get("/")
def home():
    return{
        "blog":"database is create succesfully"
    }

#create blog (protected karna hai)
@app.post("/blogs", response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate,db:Session = Depends(get_db), user=Depends(verify_token)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog



#read all blog data
@app.get("/blogs")
def get_blog(page:int=1,
             limit:int=5,
             search:str=Query(default=""),
             db:Session = Depends(get_db)):
    query = db.query(models.Blog)
    if search:
        query = query.filter(models.Blog.title.ilike(f"%{search}"))

    total = query.count()
    start = (page-1)*limit
    blogs = query.offset(start).limit(limit).all()

    return {
        "page":page,
        "limit":limit,
        "total": total,
        "data":blogs
    }    
    

#read one blog
@app.get("/blogs/{id}",response_model=schemas.BlogResponse)
def get_blogs(id:int,db: Session = Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="blog nahi hia mila")
    return blog

#update bog data (protected)
@app.put("/blogs/{id}",response_model=schemas.BlogResponse)
def update_blog(id:int,blog:schemas.BlogCreate,db: Session = Depends(get_db), user=Depends(verify_token)):
    existing_blog = db.query(models.Blog).filter(models.Blog.id==id).first()

    if not existing_blog:
            raise HTTPException(status_code=404, detail="exiting blog nahi mila")
    existing_blog.title = blog.title
    existing_blog.content = blog.content
    db.commit()
    db.refresh(existing_blog)
    return existing_blog


#delete blog data (protected)
@app.delete("/blogs/{id}")    
def delete_blog(id:int,db: Session = Depends(get_db), user= Depends(verify_token)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)

    if not blog.first():
        raise HTTPException(status_code=404, detail="exiting blog delete nahi mila")
    blog.delete()
    db.commit()
    return {
        "message":"delte this blog ok"
    }
