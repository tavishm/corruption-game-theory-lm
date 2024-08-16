import json
from pathlib import Path

## GPT generated... very bad code... @Geethika, pls correct


def generate_html(json_data, output_file="conversation_history.html"):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Conversation History</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 800px; margin: 0 auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }}
            .block-select, .bot-select {{ margin-bottom: 15px; }}
            .chat {{ margin-bottom: 20px; }}
            .chat .user {{ background-color: #d1e7fd; padding: 10px; border-radius: 8px; margin: 10px 0; text-align: right; }}
            .chat .assistant {{ background-color: #e2e2e2; padding: 10px; border-radius: 8px; margin: 10px 0; text-align: left; }}
            .chat .system {{ background-color: #f9f9f9; padding: 10px; border-radius: 8px; margin: 10px 0; font-style: italic; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Conversation History</h1>
            <div class="block-select">
                <label for="block">Select Block:</label>
                <select id="block" name="block" onchange="loadBots()">
                    {block_options}
                </select>
            </div>
            <div class="bot-select">
                <label for="bot">Select Bot:</label>
                <select id="bot" name="bot" onchange="loadConversation()">
                    {bot_options}
                </select>
            </div>
            <div id="conversation">
                {conversation_content}
            </div>
        </div>
        <script>
            const data = {script_data};
            
            function loadBots() {{
                const block = document.getElementById('block').value;
                const botSelect = document.getElementById('bot');
                botSelect.innerHTML = '';
                if(block) {{
                    data[block].forEach((bot, index) => {{
                        botSelect.innerHTML += `<option value="${{index}}">Bot ${{index+1}}</option>`;
                    }});
                }}
                loadConversation();
            }}

            function loadConversation() {{
                const block = document.getElementById('block').value;
                const botIndex = document.getElementById('bot').value;
                const conversationDiv = document.getElementById('conversation');
                conversationDiv.innerHTML = '';
                if(block && botIndex) {{
                    const context = data[block][botIndex].context;
                    context.forEach(message => {{
                        const chatClass = message.role;
                        conversationDiv.innerHTML += `<div class="chat ${{chatClass}}">${{message.content}}</div>`;
                    }});
                }}
            }}

            // Initialize the block and bot selection
            loadBots();
        </script>
    </body>
    </html>
    """

    # Building the block options
    block_options = ''.join([f'<option value="{block}">{block}</option>' for block in json_data.keys()])
    bot_options = 'sdf'
    
    # Starting conversation content empty
    conversation_content = ''

    # Format the data for the script
    script_data = json.dumps(json_data)

    # Insert the data into the HTML template
    html_content = html_content.format(
        block_options=block_options,
        bot_options=bot_options,
        conversation_content=conversation_content,
        script_data=script_data
    )

    # Save the HTML file
    Path(output_file).write_text(html_content)

    print(f"HTML file saved as {output_file}")

if __name__ == "__main__":
    # Load the JSON data
    json_file = "campaign-v1-dump-contexts.json"
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Generate the HTML
    generate_html(data)
