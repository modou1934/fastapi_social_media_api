from app import schemas
import pytest

def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/posts/")
    post = list(map(lambda post: schemas.PostWithLikes(**post),res.json()))
    assert post[0].Post.id == test_posts[0].id
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_get_one_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostWithLikes(**res.json())
    assert post.Post.id == test_posts[0].id
    assert res.status_code == 200

def test_get_one_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostWithLikes(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200

def test_get_inexistent_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/763214664")
    assert res.status_code == 404

def test_unauthorized_get_all_posts(client,test_posts):
    res = client.get("/posts/")
    assert res.status_code == 200

def test_unauthorized_get_one_post(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published",[
    ("8th title","8th content",True),
    ("9th title","9th content",False),
    ("10th title","10th content",True),
    ("11th title","11th content",False),
    ("12th title","12th content",True),
    ("13th title","13th content",False)
])
def test_create_post(authorized_client,test_posts,test_user,title,content,published):
    res = authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})
    post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.owner_id == test_user["id"]
