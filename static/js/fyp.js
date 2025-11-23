// FYP (For You Page) JavaScript for interactions

document.addEventListener('DOMContentLoaded', function() {
    initializeFYP();
});

function initializeFYP() {
    // Initialize all action buttons
    setupLikeButtons();
    setupCommentButtons();
    setupShareButtons();
    setupSaveButtons();
    setupOrderButtons();
    
    // Load comments for all posts
    loadAllComments();
}

// Like functionality
function setupLikeButtons() {
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.stopPropagation();
            const contentId = this.dataset.contentId;
            const isLiked = this.dataset.liked === 'true';
            
            try {
                const response = await fetch(`/api/fyp/content/${contentId}/like`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        action: isLiked ? 'unlike' : 'like'
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    // Update UI
                    const countEl = document.getElementById(`likes-${contentId}`);
                    if (countEl) {
                        countEl.textContent = data.likes_count;
                    }
                    
                    // Toggle liked state
                    this.dataset.liked = !isLiked;
                    this.classList.toggle('liked', !isLiked);
                }
            } catch (error) {
                console.error('Error liking content:', error);
            }
        });
    });
}

// Comment functionality
function setupCommentButtons() {
    document.querySelectorAll('.comment-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const contentId = this.dataset.contentId;
            const commentsSection = document.getElementById(`comments-section-${contentId}`);
            
            if (commentsSection) {
                const isVisible = commentsSection.style.display !== 'none';
                commentsSection.style.display = isVisible ? 'none' : 'block';
                
                // Load comments if not already loaded
                if (!isVisible) {
                    loadComments(contentId);
                }
            }
        });
    });
    
    // Setup comment submission
    document.querySelectorAll('.comment-submit').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.stopPropagation();
            const contentId = this.dataset.contentId;
            const input = document.getElementById(`comment-input-${contentId}`);
            const commentText = input.value.trim();
            
            if (!commentText) return;
            
            try {
                const response = await fetch(`/api/fyp/content/${contentId}/comment`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        comment_text: commentText,
                        username: 'User' // In a real app, get from session
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    // Clear input
                    input.value = '';
                    
                    // Update comment count
                    const countEl = document.getElementById(`comments-${contentId}`);
                    if (countEl) {
                        countEl.textContent = data.comments_count;
                    }
                    
                    // Add comment to list
                    addCommentToList(contentId, data.comment);
                }
            } catch (error) {
                console.error('Error adding comment:', error);
            }
        });
    });
    
    // Allow Enter key to submit comments
    document.querySelectorAll('.comment-input').forEach(input => {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const contentId = this.id.replace('comment-input-', '');
                const submitBtn = document.querySelector(`.comment-submit[data-content-id="${contentId}"]`);
                if (submitBtn) {
                    submitBtn.click();
                }
            }
        });
    });
}

// Share functionality
function setupShareButtons() {
    document.querySelectorAll('.share-btn').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.stopPropagation();
            const contentId = this.dataset.contentId;
            
            try {
                const response = await fetch(`/api/fyp/content/${contentId}/share`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                if (data.success) {
                    // Update share count
                    const countEl = document.getElementById(`shares-${contentId}`);
                    if (countEl) {
                        countEl.textContent = data.shares_count;
                    }
                    
                    // Try to use Web Share API if available
                    if (navigator.share) {
                        const post = document.querySelector(`.fyp-post[data-content-id="${contentId}"]`);
                        const title = post.querySelector('.post-title')?.textContent || 'Check out this halal food!';
                        const description = post.querySelector('.post-description')?.textContent || '';
                        
                        navigator.share({
                            title: title,
                            text: description,
                            url: window.location.href
                        }).catch(err => console.log('Error sharing:', err));
                    } else {
                        // Fallback: copy to clipboard
                        const url = window.location.href;
                        navigator.clipboard.writeText(url).then(() => {
                            alert('Link copied to clipboard!');
                        });
                    }
                }
            } catch (error) {
                console.error('Error sharing content:', error);
            }
        });
    });
}

// Save functionality
function setupSaveButtons() {
    document.querySelectorAll('.save-btn').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.stopPropagation();
            const contentId = this.dataset.contentId;
            const isSaved = this.dataset.saved === 'true';
            
            try {
                const response = await fetch(`/api/fyp/content/${contentId}/save`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        action: isSaved ? 'unsave' : 'save'
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    // Update UI
                    const countEl = document.getElementById(`saves-${contentId}`);
                    if (countEl) {
                        countEl.textContent = data.saves_count;
                    }
                    
                    // Toggle saved state
                    this.dataset.saved = !isSaved;
                    this.classList.toggle('saved', !isSaved);
                }
            } catch (error) {
                console.error('Error saving content:', error);
            }
        });
    });
}

// Order functionality (Most Important)
function setupOrderButtons() {
    document.querySelectorAll('.order-btn').forEach(btn => {
        btn.addEventListener('click', async function(e) {
            e.stopPropagation();
            const contentId = this.dataset.contentId;
            const restaurantId = this.dataset.restaurantId;
            const orderUrl = this.dataset.orderUrl;
            
            try {
                const response = await fetch(`/api/fyp/content/${contentId}/order`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                if (data.success) {
                    // Redirect to order page
                    if (data.order_url) {
                        window.location.href = data.order_url;
                    } else if (data.restaurant_id) {
                        window.location.href = `/restaurants/${data.restaurant_id}`;
                    } else {
                        alert(`Order from ${data.restaurant_name}!`);
                    }
                } else {
                    alert('Unable to process order. Please try again.');
                }
            } catch (error) {
                console.error('Error processing order:', error);
                // Fallback: try to navigate to restaurant page
                if (restaurantId) {
                    window.location.href = `/restaurants/${restaurantId}`;
                } else if (orderUrl) {
                    window.location.href = orderUrl;
                }
            }
        });
    });
}

// Load comments for a specific post
async function loadComments(contentId) {
    const commentsList = document.getElementById(`comments-list-${contentId}`);
    if (!commentsList) return;
    
    // Check if already loaded
    if (commentsList.dataset.loaded === 'true') return;
    
    try {
        const response = await fetch(`/api/fyp/content/${contentId}/comments`);
        const comments = await response.json();
        
        commentsList.innerHTML = '';
        if (comments.length === 0) {
            commentsList.innerHTML = '<p style="color: rgba(255,255,255,0.6); font-size: 14px; padding: 10px;">No comments yet. Be the first!</p>';
        } else {
            comments.forEach(comment => {
                addCommentToList(contentId, comment);
            });
        }
        
        commentsList.dataset.loaded = 'true';
    } catch (error) {
        console.error('Error loading comments:', error);
        commentsList.innerHTML = '<p style="color: rgba(255,255,255,0.6); font-size: 14px; padding: 10px;">Error loading comments.</p>';
    }
}

// Add a comment to the list
function addCommentToList(contentId, comment) {
    const commentsList = document.getElementById(`comments-list-${contentId}`);
    if (!commentsList) return;
    
    // Remove "no comments" message if present
    const noCommentsMsg = commentsList.querySelector('p');
    if (noCommentsMsg && noCommentsMsg.textContent.includes('No comments')) {
        noCommentsMsg.remove();
    }
    
    const commentEl = document.createElement('div');
    commentEl.className = 'comment-item';
    commentEl.innerHTML = `
        <span class="comment-username">${escapeHtml(comment.username)}</span>
        <span class="comment-text">${escapeHtml(comment.comment_text)}</span>
    `;
    
    commentsList.insertBefore(commentEl, commentsList.firstChild);
}

// Load all comments (for initial load)
function loadAllComments() {
    document.querySelectorAll('.fyp-post').forEach(post => {
        const contentId = post.dataset.contentId;
        // Comments will be loaded when user clicks comment button
    });
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Smooth scroll behavior
let isScrolling = false;
const fypFeed = document.getElementById('fypFeed');

if (fypFeed) {
    fypFeed.addEventListener('scroll', function() {
        if (!isScrolling) {
            window.requestAnimationFrame(function() {
                isScrolling = false;
            });
            isScrolling = true;
        }
    });
}

// Keyboard navigation (optional)
document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowDown' || e.key === 'PageDown') {
        e.preventDefault();
        const currentPost = document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2);
        const nextPost = currentPost?.closest('.fyp-post')?.nextElementSibling;
        if (nextPost) {
            nextPost.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
        e.preventDefault();
        const currentPost = document.elementFromPoint(window.innerWidth / 2, window.innerHeight / 2);
        const prevPost = currentPost?.closest('.fyp-post')?.previousElementSibling;
        if (prevPost) {
            prevPost.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
});

