document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#user').style.display = 'none';

    if (document.getElementById('following')) {
        document.getElementById('following').addEventListener('click', () => posts_view('/followed', 1));
    } else {
        document.getElementById('new_post').addEventListener('click', () => login());
    }

    posts_view('', 1);
})

function posts_view(path, page) {
    if (path.includes('?')) {
        path += `&page=${page}`;
    } else {
        document.querySelector('#user').style.display = 'none';
        path += `?page=${page}`;
    }

    fetch(`/posts${path}`)
    .then(response => response.json())
    .then(response => {
        document.getElementById('posts').innerHTML = '';
        get_pagination(path, page, response.num_pages);
        response.posts.forEach(post => post_create(post));
    })
}

function get_pagination(path, page, numPages) {
    pages = document.getElementById('pagination');
    pages.className = 'pagination justify-content-center';
    pages.innerHTML = '';

    let previous = document.createElement('li');
    if (page == 1) {
        previous.className = 'page-item disabled';
    } else {
        previous.className = 'page-item';
        previous.addEventListener('click', () => posts_view(path, page-1));
    }

    pages.append(previous);

    let previousPage = document.createElement('a');
    previousPage.className = 'page-link';
    previousPage.href = '#';
    previousPage.innerHTML = 'Previous';

    previous.append(previousPage);

    for (let item = 1; item <= numPages; item++) {
        let icon = document.createElement('li');
        if (item == page) {
            icon.className = 'page-item active';
        } else {
            icon.className = 'page-item';
            icon.addEventListener('click', () => posts_view(path, item));
        }

        let link = document.createElement('a');
        link.className = 'page-link';
        link.href = '#';
        link.innerHTML = item;

        icon.append(link);
        pages.append(icon);
    }

    let next = document.createElement('a');
    if (page == numPages) {
        next.className = 'page-item disabled';
    } else {
        next.className = 'page-item';
        next.addEventListener('click', () => posts_view(path, page+1));
    }

    let nextPage = document.createElement('a');
    nextPage.className = 'page-link';
    nextPage.href = '#';
    nextPage.innerHTML = 'Next';

    next.append(nextPage);
    pages.append(next);
}

function post_create(post) {
    let card = document.createElement('div');
    card.className = 'card text-center';

    let cardHeader = document.createElement('div');
    cardHeader.className = 'card-header';
    cardHeader.innerHTML = `
        <strong>${post.author_username}</strong> 
        &nbsp;  &nbsp; &nbsp;  &nbsp; 
        <small class="text-muted">${post.date_created}</small>
    `;
    card.append(cardHeader);
    cardHeader.addEventListener('click', () => user_details_view(post.author_id));

    let cardBody = document.createElement('div');
    cardBody.className = 'card-body';
    cardBody.id = `post_body_${post.post_id}`;

    let cardText = document.createElement('p');
    cardText.className = 'card-text';
    cardText.id = `post_${post.post_id}`;
    cardText.innerHTML = post.post;
    
    cardBody.append(cardText);

    let likesRow = document.createElement('div');
    likesRow.id = `likes_row_${post.post_id}`;
    likesRow.className = 'row justify-content-center';

    let likeIcon = document.createElement('i');
    likeIcon.id = `like-icon-${post.post_id}`;
    let iconBg;
    if(post.liked) {
        iconBg='';
    } else {
        iconBg='-empty';
    }
    likeIcon.className = `icon-heart${iconBg} col-auto`;
    if (document.getElementById('following')) {
        likeIcon.addEventListener('click', () => post_like(post));        
    } else {
        likeIcon.addEventListener('click', () => login());
    }
    
    likesRow.append(likeIcon);

    let likes = document.createElement('div');
    likes.id = `likes-number-${post.post_id}`;
    likes.className = 'card-text likes col-auto';
    likes.innerHTML = post.likes;
    
    likesRow.append(likes);

    let likesText = document.createElement('div');
    likesText.className = 'card-text col-auto text-center';
    likesText.innerHTML = 'like(s)';
    
    likesRow.append(likesText);

    if (post.is_editable) {
        let editBtn = document.createElement('button');
        editBtn.className = 'card-text col-auto btn btn-primary';
        editBtn.innerHTML = 'Edit Post';
        editBtn.addEventListener('click', () => post_edit(post));

        likesRow.append(editBtn);
    }

    cardBody.append(likesRow);
    card.append(cardBody);

    let row = document.createElement('div');
    row.className = 'row justify-content-center';
    row.append(card);

    document.querySelector('#posts').append(row);
}

function post_edit(post) {
    let likesRow = document.getElementById(`likes_row_${post.post_id}`);    
    let postContent = document.getElementById(`post_${post.post_id}`);
        
    let postBody  = postContent.parentNode;    

    let editBtnRow = document.createElement('div');
    editBtnRow.className = 'row';

    let postEditable = document.createElement('input');
    postEditable.id = `new_post_${post.post_id}`;
    postEditable.type = 'textarea';
    postEditable.className = 'form-control';
    postEditable.value = postContent.innerHTML;
    
    document.getElementById(`likes_row_${post.post_id}`).remove();
    document.getElementById(`post_${post.post_id}`).remove();
    
    editBtnRow.append(postEditable);

    let extraSpace = document.createElement('div');
    extraSpace.innerHTML = `<br>`;
    editBtnRow.append(extraSpace);

    let saveBtn = document.createElement('button');
    saveBtn.className = 'btn btn-success col-auto';
    saveBtn.type = 'button';
    saveBtn.innerHTML = 'Save Post';
    saveBtn.addEventListener('click', () => {
        let new_post = document.getElementById(`new_post_${post.post_id}`).value;

        fetch(`/post/create_edit`, {
            method: 'PUT',
            headers: {
                'X-CSRFToken': get_cookie('csrftoken')
            },
            body: body = JSON.stringify({
                post_id: post.post_id,
                new_post: new_post
            })
        })
        .then(response => response.json())
        .then(response => {
            if (response.result) {
                postContent.innerHTML = new_post;
            } else {
                alert('You do not have permission to edit this post');
            }
            editBtnRow.remove();
            postEditable.remove();

            postBody.append(postContent);
            postBody.append(likesRow);
        })
    })

    editBtnRow.append(saveBtn);

    let cancelBtn = document.createElement('button');
    cancelBtn.className = 'btn btn-secondary col-auto';
    cancelBtn.type = 'button';
    cancelBtn.innerHTML = 'Cancel';
    cancelBtn.addEventListener('click', () => {
        editBtnRow.remove();
        post_editable.remove();
        postBody.append(postContent);
        postBody.append(likesRow);                  
    });
    editBtnRow.append(cancelBtn);
    postBody.appendChild(editBtnRow); 
}

function post_like(post) {
    fetch(`post/${post.post_id}/like`)
    .then(response => response.json())
    .then(response => {
        if (response.liked) {
            document.getElementById(`like-icon-${post.post_id}`).className = 'icon-heart col-auto';
        } else {
            document.getElementById(`like-icon-${post.post_id}`).className = 'icon-heart-empty col-auto';
        }
        document.getElementById(`likes-number-${post.post_id}`).innerHTML=response.new_number;
    })
}

function user_details_view(author_id) {
    posts_view(`?user=${author_id}`, 1);

    document.querySelector('#new_post').style.display = 'none';
    followBtn = document.getElementById('follow-btn');
    followBtn.style.display = 'none'; 
    document.querySelector('#user').style.display = 'block';

    fetch(`/user/${author_id}`)
    .then(response => response.json())
    .then(user => {
        document.getElementById('following-number').innerHTML = user.following;
        document.getElementById('followers-number').innerHTML = user.followers;
        document.getElementById('username').innerHTML = user.username;

        if (user.can_follow) {
            followBtn.style.display = 'unset';
            if (user.currently_following) {
                followBtn.innerHTML = 'Unfollow';
            } else {
                followBtn.innerHTML = 'Follow';
            }
            followBtn.addEventListener('click', () => user_follow(author_id));
        }
    })
    window.scrollTo(0, 0);
}

function user_follow(user_id) {
    fetch(`user/${user_id}/follow`)
    .then(response => response.json())
    .then(response => {
        followBtn = document.getElementById('follow-btn');
        if (response.new_follower) {
            followBtn.innerHTML = 'Unfollow';
        } else {
            followBtn.innerHTML = 'Follow';
        }
        document.getElementById('followers-number').innerHTML = response.new_number;
    })
}

function login() {
    document.getElementById('login').click();
}

function get_cookie(cookieName) {
    let cookieVal = `; ${document.cookie}`;
    let cookieParts = cookieVal.split(`; ${cookieName}=`);
    if (cookieParts.length === 2) {
        return cookieParts.pop().split(';').shift();
    }
}