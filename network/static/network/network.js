document.addEventListener('DOMContentLoaded', function() {

    // When the edit post button is clicked
    document.querySelectorAll('.edit-post').forEach(edit => edit.addEventListener('click', function(e) {
        e.preventDefault();

        // Get csrf token value and post id
        const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        const post = this.parentElement.parentElement;
        const id = post.children[2].value;

        // Hide the current post details and show the edit post div
        post.style.display = 'none';
        editDiv = post.parentElement.children[2];
        editDiv.style.display = 'block';

        // When the save button is clicked
        document.querySelectorAll("#save-btn").forEach(btn => btn.addEventListener('click', function(e) {
            e.preventDefault();

            // Get what the user has typed in the textarea
            var edited = post.parentElement.children[2].children[0].value;
            
            // Send a PUT request to modify the content value of the post to the edited value
            fetch(`/posts/${id}`, {
                method: "PUT",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    content: `${edited}`
                })
            })

            // Hide the edit post div and show the post details with the new edited content
            editDiv.style.display = 'none';
            post.style.display = 'block';
            post.children[0].innerHTML = edited;
        }))        
    }))


    // When the heart icon is clicked
    document.querySelectorAll('#heart-symbol').forEach(heart => heart.addEventListener('click', function(e) {
        e.preventDefault();

        // Get csrf token value and post id
        const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        const post = this.parentElement.parentElement;
        const id = post.children[2].value;

        // Get the like count and the anchor tag which containts the svg icon
        var likes = parseInt(post.children[4].children[1].innerHTML);
        const anchor = post.children[4].children[0];

        // Check which heart icon is being showed in order to change to the other one when the heart icon is clicked
        if (anchor.children[0].classList.contains("bi-heart")) {
            anchor.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart-fill" viewBox="0 0 16 16">
            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
          </svg>`;
        }

        else {
            anchor.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
            <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
        </svg>`;
        }


        fetch(`/posts/${id}`)
        .then(response => response.json())
        .then(results => {

            // Get the list of users' ids that like this post
            var initial = results.likes;
            var user = parseInt(post.children[3].value);
            
            // Check if the user already likes the post. If he does it means he unliked the post
            // Remove him from the list and reduce number of likes by 1
            if (initial.includes(user)) {
                const index = initial.indexOf(user);
                initial.splice(index, 1);
                likes--;
            }

            else {
                initial.push(user);
                likes++;
            }

            // Send a PUT request to modify the list of users who like the post
            fetch(`/posts/${id}`, {
                method: "PUT",
                headers: {'X-CSRFToken': csrf},
                body: JSON.stringify({
                    likes: `${initial}`
                })
            })

            // Set the like count to the updated one
            post.children[4].children[1].innerHTML = likes;
        })  
    }))
})