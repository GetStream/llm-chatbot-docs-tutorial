css = """
<style>
.chat-message {
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e5e5;
  margin-top: 1rem;
}

.chat-message h3 {
  font-size: medium;
  font-weight: bold;
  color: #919191;
  margin-bottom: 0;
  padding-bottom: 0;
}

.user-message {
    background: aliceblue;
}
</style>
"""

bot_template = """
<div class="chat-message">
  <h3>Documentation bot</h3>
  <p>{{MSG}}</p>
</div>
"""

user_template = """
<div class="chat-message user-message">
  <h3>User</h3>
  <p>{{MSG}}</p>
</div>
"""
