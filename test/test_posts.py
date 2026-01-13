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

def test_unauthorized_user_delete_post(client,test_user, test_posts):
    res= client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_authorized_user_delete_post(authorized_client,test_user, test_posts):
    res= authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_authorized_user_delete_not_existing_post(authorized_client,test_user, test_posts):
    res= authorized_client.delete(f"/posts/252335")
    assert res.status_code == 404

def test_authorized_other_user_delete_not_existing_post(authorized_client,test_user, test_posts):
    res= authorized_client.delete(f"/posts/{test_posts[7].id}")
    assert res.status_code == 403

def test_authorized_user_update_post(authorized_client,test_user, test_posts):
    data = {"title":"0 title","content":"0 content"}
    res= authorized_client.put(f"/posts/{test_posts[4].id}",json=data)
    updated_posts= schemas.Post(**res.json())
    assert updated_posts.title == data["title"]
    assert updated_posts.content == data["content"]

def test_authorized_other_user_update_post(authorized_client,test_user, test_posts):
    data = {"title":"00 title","content":"0 content"}
    res= authorized_client.put(f"/posts/{test_posts[7].id}",json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client,test_user, test_posts):
    data = {"title":"0 title","content":"0 content"}
    res= client.put(f"/posts/{test_posts[4].id}",json=data)
    assert res.status_code == 401

def test_authorized_user_update_not_existing_post(authorized_client,test_user, test_posts):
    data = {"title":"0 title","content":"0 content"}
    res= authorized_client.put(f"/posts/35225",json=data)
    assert res.status_code == 404