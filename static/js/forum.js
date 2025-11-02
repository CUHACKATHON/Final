// Forum functionality
(function() {
    // Get session ID from localStorage (same as chat)
    let sessionId = localStorage.getItem('chatSessionId');
    
    // Create post form
    const createPostBtn = document.getElementById('create-post-btn');
    const createPostForm = document.getElementById('create-post-form');
    const postForm = document.getElementById('post-form');
    const cancelPostBtn = document.getElementById('cancel-post-btn');

    if (createPostBtn && createPostForm) {
        createPostBtn.addEventListener('click', () => {
            createPostForm.style.display = createPostForm.style.display === 'none' ? 'block' : 'none';
        });

        if (cancelPostBtn) {
            cancelPostBtn.addEventListener('click', () => {
                createPostForm.style.display = 'none';
                postForm.reset();
            });
        }

        if (postForm) {
            postForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const title = document.getElementById('post-title').value.trim();
                const content = document.getElementById('post-content').value.trim();
                
                if (!title || !content) {
                    alert('Please fill in both title and content.');
                    return;
                }

                try {
                    const response = await fetch('/api/forum/posts/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            session_id: sessionId,
                            title: title,
                            content: content
                        })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        alert(data.message);
                        postForm.reset();
                        createPostForm.style.display = 'none';
                        // Reload page to show new post if approved
                        setTimeout(() => location.reload(), 1000);
                    } else {
                        alert('Error: ' + (data.error || 'Failed to create post'));
                    }
                } catch (error) {
                    alert('Connection error. Please try again.');
                    console.error('Error:', error);
                }
            });
        }
    }

    // Reply form
    const replyForm = document.getElementById('reply-form');
    if (replyForm) {
        replyForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const postId = document.getElementById('post-id').value;
            const content = document.getElementById('reply-content').value.trim();
            
            if (!content) {
                alert('Please enter a reply.');
                return;
            }

            try {
                const response = await fetch(`/api/forum/posts/${postId}/replies/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        session_id: sessionId,
                        content: content
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    alert(data.message);
                    replyForm.reset();
                    // Reload page to show new reply if approved
                    setTimeout(() => location.reload(), 1000);
                } else {
                    alert('Error: ' + (data.error || 'Failed to create reply'));
                }
            } catch (error) {
                alert('Connection error. Please try again.');
                console.error('Error:', error);
            }
        });
    }
<<<<<<< HEAD

    // Like functionality
    function getOrCreateSessionId() {
        let sessionId = localStorage.getItem('chatSessionId');
        if (!sessionId) {
            // Generate a new UUID v4
            sessionId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                const r = Math.random() * 16 | 0;
                const v = c === 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
            localStorage.setItem('chatSessionId', sessionId);
        }
        return sessionId;
    }

    // Handle like buttons
    document.addEventListener('click', async (e) => {
        if (e.target.closest('.like-btn')) {
            const likeBtn = e.target.closest('.like-btn');
            const postId = likeBtn.getAttribute('data-post-id');
            const sessionId = getOrCreateSessionId();
            
            if (!postId) return;
            
            // Disable button during request
            likeBtn.disabled = true;
            
            try {
                const response = await fetch(`/api/forum/posts/${postId}/like/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        session_id: sessionId
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    // Update UI
                    const likesCountEl = likeBtn.querySelector('.likes-count');
                    const likeIconEl = likeBtn.querySelector('.like-icon');
                    
                    if (likesCountEl) {
                        likesCountEl.textContent = data.likes_count;
                    }
                    
                    // Toggle liked state
                    if (data.liked) {
                        likeBtn.classList.add('liked');
                        if (likeIconEl) {
                            likeIconEl.textContent = '❤️';
                        }
                    } else {
                        likeBtn.classList.remove('liked');
                        if (likeIconEl) {
                            likeIconEl.textContent = '🤍';
                        }
                    }
                } else {
                    alert('Error: ' + (data.error || 'Failed to like post'));
                }
            } catch (error) {
                alert('Connection error. Please try again.');
                console.error('Error:', error);
            } finally {
                likeBtn.disabled = false;
            }
        }

        // Handle share buttons
        if (e.target.closest('.share-btn')) {
            const shareBtn = e.target.closest('.share-btn');
            const postId = shareBtn.getAttribute('data-post-id');
            const sessionId = getOrCreateSessionId();
            
            if (!postId) return;
            
            // Build share URL
            const shareUrl = window.location.origin + `/forum/post/${postId}/`;
            
            // Try Web Share API first (mobile)
            if (navigator.share) {
                try {
                    await navigator.share({
                        title: document.querySelector('h1, h3')?.textContent || 'Forum Post',
                        text: 'Check out this post on MoodLift',
                        url: shareUrl
                    });
                    
                    // Track share
                    await fetch(`/api/forum/posts/${postId}/share/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            session_id: sessionId,
                            platform: 'native'
                        })
                    });
                } catch (error) {
                    if (error.name !== 'AbortError') {
                        // User cancelled or error, fallback to copy
                        fallbackShare(shareUrl, postId, sessionId);
                    }
                }
            } else {
                // Fallback to copy to clipboard
                fallbackShare(shareUrl, postId, sessionId);
            }
        }
    });

    // Fallback share function
    async function fallbackShare(url, postId, sessionId) {
        try {
            // Copy to clipboard
            await navigator.clipboard.writeText(url);
            alert('Link copied to clipboard!');
            
            // Track share
            const response = await fetch(`/api/forum/posts/${postId}/share/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    platform: 'copy'
                })
            });

            if (response.ok) {
                const data = await response.json();
                // Update shares count
                const shareBtn = document.querySelector(`.share-btn[data-post-id="${postId}"]`);
                if (shareBtn) {
                    const sharesCountEl = shareBtn.querySelector('.shares-count');
                    if (sharesCountEl) {
                        sharesCountEl.textContent = data.shares_count;
                    }
                }
            }
        } catch (error) {
            // Final fallback: show URL in prompt
            prompt('Copy this link to share:', url);
            
            // Still track the share
            try {
                await fetch(`/api/forum/posts/${postId}/share/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        session_id: sessionId,
                        platform: 'manual'
                    })
                });
            } catch (err) {
                console.error('Error tracking share:', err);
            }
        }
    }
=======
>>>>>>> bd11b21620787d7a385999cc098de119c036ce3a
})();

