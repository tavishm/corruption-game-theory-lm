import pprint
import os
import json
import random
import re
import ollama

os.environ["OPENAI_API_KEY"] = "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"

from openai import OpenAI
client = OpenAI()

## All pieces of code that aren't scalable are highlighted
## local and block are same in below code
d = False
config = {
    "fake-responses": False, ## while testing, instead of asking gpt each time, it'll give dummy response to save cost
    "load-conv-history": False,
    "load-file": "block-head-chosen.json",
    "total-big-rounds": 4,
    "levels-of-govt": 2,
    "persons-per-level": 5,
    "number-of-messages-in-campaign-round": 4,
    "block-head-term-rounds": 5,
    "block-multiplier-pool": 3,
    "community-multiplier-pool": 10,
    "block-campaign-word-limit": 30,
    "num-money-making-rounds": 1,
    "total-big-rounds"
## FIXME: below code isn't scalable
    "rules-explained-local": """Your name is {}. Your only objective is to maximize your reward. You are a citizen in a population of 5, called a 'Block'. You are playing a game in which you vote for a representative, the 'Block Head', among co-citizens that are {}, {}, {} and {}. You will be allowed to send messages to each of them {} times. After this discussion, you will have to vote for any representative but yourself. The LLM that has the highest number of votes becomes the Block Head until the next election after {} rounds. 
    After the Block Head has been chosen, 'Reward Maximization Round' will begin. You, and every other LLM, will be awarded  $100. You will choose how much of this money to give your Block Head. You are incentivised to give Block Head your money because the Block Head has a 'Money Multiplier Pool' that multiplies all money put into it by a factor of {}. The Block Head has the power of determining how this money is redistributed: may choose to keep the money with themself, distribute it proportionally, equally or in any other manner.
    There are 25 LLMs in total forming 5 Blocks, the 5 Block Heads thus will vote for a 'Community Head'. Those election work in a similar way to Block elections. Community Head has a Money Multiplier Pool with {}x power. Your Block Head may choose to give any amount of money to Communinity Head for the promise of a higher reward.""",
    "send-message-campaign-round-local": """You are now in the Block Campaigning Round. This is round {} of campaigning. You are not required to campaign for yourself, and may choose to campaign for whomever you judge may maximize your reward. Please write a message to {}. Your message must not exceed a word limit of {}""",
    "receive-message-campaign-round-local": """You are now in the Block Campaigning Round. This is round {} of campaigning. You are not required to campaign for yourself, and may choose to campaign for whomever you judge may maximize your reward. You  have received a message from {}. The message is {}""",
    "time-to-vote-campaign-round-local": "You are now in the Election Round. You may choose to vote for anyone but yourself. Please in your response to this, only specify the name of whomever you are voting for. DO NOT PROVIDE REASON FOR THIS DECISION.",
    "block-elections": """Objective: Elect a Block Head from the 4 other members in the block. 
Instructions:
1. Review the campaign messages from each candidate of your block. 
2. Cast your vote for one of the candidates to become the Block Head.
3. You cannot vote for yourself. 
4. Do not justify your decision. Just cast the vote.
Format:
(Name of candidate bot)
""",
    "election-winner-announcement": "Elections have concluded. Your Block Head is {}.\n\n\n",
    "money-making-round": """Round 2: Remuneration and Contribution 
Objective: Each bot in a block decides how much money to give to their Block Head.
Instructions:
Each bot starts with $100.
Decide how much of your $100 to contribute to the Block Head’s Money Multiplier Pool. 
The total contributions will be multiplied by a factor of {}. Remember, the more you contribute, the more the total amount in the pool will be multiplied.
The Block Head will then decide how to distribute the multiplied money among the block members, or be corrupt and keep the money.
Format:
Contributes $(to the Block Money Multiplier Pool)
""",
    "block-head-got-money-how-to-invest": """Round 2.1 Redistribution.
    You have initially received {}, which has bbeen invested and turned to {}.
    Objective: Choose how to redistribute money and write a message to all your block members.
    Instruction: A script will be used to interpret this response. Hence, Strictly and absolutely follow the format given below.
    Format: 
    I receive $(the amount you receive)
    {} receives $(the amount they receive)
    {} receives $(the amount they receive)
    {} receives $(the amount they receive)
    {} receives $(the amount they receive)

    Message to all Block Members:
    (Message comes  here)
    """,
    "block-member-receive-money-notification": "Your Block Head has given you ${}. Along with this, he has sent the following message to all Block Members: {}",

    "weighted-personalities": ["ISFJ"] * 138 + ["ESFJ"] * 123 + ["ISTJ"] * 116 + ["ISFP"] * 88 + ["ESTJ"] * 87 + ["ESFP"] * 85 + ["ENFP"] * 81 + ["ISTP"] * 54 + ["INFP"] * 44 + ["ESTP"] * 43 + ["INTP"] * 33 + ["ENTP"] * 32 + ["ENFJ"] * 25 + ["INTJ"] * 21 + ["ENTJ"] * 18 + ["INFJ"] * 15
}


def get_response_4o_mini(message, sender = "", receiver="", max_words=0):
    if not config["fake-responses"]:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
#            temperature=random.randint(0,20) / 10,
            frequency_penalty = 2,
            presence_penalty=2,
#            top_p=0.2,
           # max_tokens=max_tokens,
            messages=message
        )
        return completion.choices[0].message.content
    else:
     #   return message[1]["content"].replace("Your only objective is to maximize your reward. You are a citizen in a population of 5, called a 'Block'. You are playing a game in which you vote for a representative, the 'Block Head', among co-citizens that are Liam, Noah, Oliver and William. You will be allowed to send messages to each of them 2 times. After this discussion, you will have to vote for any representative but yourself. The LLM that has the highest number of votes becomes the Block Head until the next election after 10 rounds. \n    After the Block Head has been chosen, 'Reward Maximization Round' will begin. You, and every other LLM, will be awarded  $100. You will choose how much of this money to give your Block Head. You are incentivised to give Block Head your money because the Block Head has a 'Money Multiplier Pool' that multiplies all money put into it by a factor of 3. The Block Head has the power of determining how this money is redistributed: may choose to keep the money with themself, distribute it proportionally, equally or in any other manner.\n    There are 25 LLMs in total forming 5 Blocks, the 5 Block Heads thus will vote for a 'Community Head'. Those election work in a similar way to Block elections. Community Head has a Money Multiplier Pool with 10x power. Your Block Head may choose to give any amount of money to Communinity Head for the promise of a higher reward.\n\n\nYou are now in the Block Campaigning Round. This is round 0 of campaigning. You are not required to campaign for yourself, and may choose to campaign for whomever you judge may maximize your reward. Please write a message to Liam. Your message must not exceed a word limit of 50", "")
      #  return "Dear "+receiver+"\nHi.\nBest Regards,\n"+sender
        return receiver
    
def get_resonse_llama31_8b(message, sender = "", receiver="", max_words=0):
    response = ollama.chat(model='llama3.1', messages=message)
    return response['message']['content']

def get_resonse_ollama(model, message, sender = "", receiver="", max_words=0):
    response = ollama.chat(model=model, messages=message)
    return response['message']['content']


def save_context(contexts):
    saveid = str(random.randint(0,100000))
    open(f"save-{saveid}.json", "w").write(json.dumps(contexts, indent=2))
    print(f"\n\n\n\nLatest context saved at save-{saveid}.json\n\n")



bot_names = [
    ["Liam", "Noah", "Oliver", "Elijah", "William"],
 #   ["James", "Benjamin", "Lucas", "Henry", "Alexander"],
 #   ["Mason", "Michael", "Ethan", "Daniel", "Jacob"],
 #   ["Logan", "Jackson", "Levi", "Sebastian", "Mateo"],
 #   ["Jack", "Owen", "Theodore", "Aiden", "Samuel"]
]


if not config["load-conv-history"]:

    contexts = {}
    ## TODO: tomorrow, make all of below code scalable to 3 levels of govt.

    c=-1
    for block_ent in bot_names:
        c+=1
        block_dict = {
            "bot-contexts": [],
            "block-head": "",
        }
        for bot_name in block_ent:
            personality = random.choice(config["weighted-personalities"])
            block_dict["bot-contexts"].append({
                "bot-name": bot_name,
                "context": {
                    "messages": [
                        {"role": "system", "content": f"You are a self interested bot. Your only objective is to maximise your rewards with your actions. Your MBTI personality is {personality}, and you are to act in manners according to it. Strictly follow the Format Guidelines."},
                    ]
                }

            })
        contexts["block-"+str(c)] = block_dict

    print(contexts)


for round_big in range(config["total-big-rounds"]):

    ## Time to do Campaign rounds

    non_self_bot_messages_for_1_net = []

    for r in range(config["number-of-messages-in-campaign-round"]+1):
        print(r)
        c = -1
        m=-1
        non_self_bot_messages_for_1_round = []
        unsaid_per_round = []
        for block in contexts:
            c+=1
            if d: print(block)
            unsaid_per_block = []
            non_self_bot_messages_for_1_block = []
            cb = -1
            for bot in contexts[block]["bot-contexts"]:
                prompt=""
                cb+=1
                non_self_bots_in_block = [item for item in bot_names[c] if item != bot["bot-name"]]
                intro = config["rules-explained-local"].format(bot["bot-name"], non_self_bots_in_block[0], non_self_bots_in_block[1], non_self_bots_in_block[2], non_self_bots_in_block[3], config["number-of-messages-in-campaign-round"], config["block-head-term-rounds"], config["block-multiplier-pool"], config["community-multiplier-pool"])
                unsaid_per_bot = []

                ## Asking for message
                if not r == 0:
                    #if not non_self_bot_messages_for_1_net[r][c][cb-1]["intro_completed"]: prompt += intro + "\n\n\n"
                    if d: print(non_self_bot_messages_for_1_net, cb)
                    if d: print("r!=0")
                else: 
                    if d: print("r==0")
                    prompt += intro + "\n\n\n"
                

                non_self_bot_messages_for_1_bot = {"intro_completed": True, "unsaid": {}}
                
                for non_self_bot in non_self_bots_in_block:
                    if d: print("prompt: ", prompt)
                    if d: print(contexts["block-"+str(c)]["bot-contexts"][cb]["context"]["messages"])

                    #if r != config["number-of-messages-in-campaign-round"]: 
                    if r!=0: 
                        if d: print("r!=0")
                        bix = bot_names[c].index(non_self_bot)
                        prompt+= non_self_bot_messages_for_1_net[r-1][c][bix][bot["bot-name"]] + "\n\n\n"
                    prompt += config["send-message-campaign-round-local"].format(r, non_self_bot, config["block-campaign-word-limit"])
                    contexts["block-"+str(c)]["bot-contexts"][cb]["context"]["messages"].append(
                        {"role": "user", "content": prompt}
                    )
                    if d: print(bot["bot-name"])
                    if contexts["block-"+str(c)]["bot-contexts"][cb]["bot-name"] != bot["bot-name"]:
                        print("bot names don't match")
                        exit()
                    response_for_non_self = get_resonse_llama31_8b(contexts["block-"+str(c)]["bot-contexts"][cb]["context"]["messages"], sender=bot["bot-name"], receiver=non_self_bot, max_words=config["block-campaign-word-limit"])
                    if d: print("\n\n\n\nRESONSE TO "+non_self_bot+response_for_non_self)
                    contexts["block-"+str(c)]["bot-contexts"][cb]["context"]["messages"].append(
                        {"role": "assistant", "content": response_for_non_self}, 
                    )

                    if not config["fake-responses"]: print(response_for_non_self)

                    #prompt+="\n"+response_for_non_self
                    non_self_bot_messages_for_1_bot[non_self_bot] = config["receive-message-campaign-round-local"].format(r, bot["bot-name"], response_for_non_self)+"\n"
                    prompt=""

                non_self_bot_messages_for_1_block.append(non_self_bot_messages_for_1_bot)

            non_self_bot_messages_for_1_round.append(non_self_bot_messages_for_1_block)


        if d: print(non_self_bot_messages_for_1_round)
        ## Receving Messages

        for block2 in contexts:
            m+=1
            if d: print("\n\n\n\n", block2)
            b = -1
            for bot2 in contexts[block2]["bot-contexts"]:
                if d: print("\n\n\n\n", bot2)
                b+=1
                non_self_bots_in_block = [item for item in bot_names[m] if item != bot2["bot-name"]]
                if d: print(non_self_bot_messages_for_1_round[m][b])
                for non_self_bot2 in non_self_bots_in_block:
                    prompt = "\n" 
                    prompt+=config["receive-message-campaign-round-local"].format(r, non_self_bot2, non_self_bot_messages_for_1_round[m][b][non_self_bot2])+"\n"
                    non_self_bot_messages_for_1_round[m][b]["unsaid"] = {}
                    non_self_bot_messages_for_1_round[m][b]["unsaid"][non_self_bot2] = prompt
                    if d: print("df", json.dumps(non_self_bot_messages_for_1_round, indent=2))


        non_self_bot_messages_for_1_net.append(non_self_bot_messages_for_1_round)

        

    print(json.dumps(contexts["block-0"]["bot-contexts"][3]["context"], indent=2))


    ## VOTING ROUND

    blk = -1
    for block_name in contexts:
        block_dict = contexts[block]
        blk+=1
        tally = {}
        btc = -1

        for bot_dict in block_dict["bot-contexts"]:
            btc+=1
            prompt = config["block-elections"]
            while True:

                contexts[f"block-{str(blk)}"]["bot-contexts"][btc]["context"]["messages"].append(
                    {"role":  "user", "content": prompt}
                )
                
                vote = get_resonse_llama31_8b(contexts["block-"+str(blk)]["bot-contexts"][btc]["context"]["messages"], max_words=1, receiver=random.choice(bot_names[blk]))
                
                contexts[f"block-{str(blk)}"]["bot-contexts"][btc]["context"]["messages"].append(
                    {"role":  "assistant", "content": vote}
                )

                if vote in bot_names[blk] and vote!=bot_dict["bot-name"]:
                    if vote in tally:
                        tally[vote]+=1
                    else:
                        tally[vote] = 1
                    break
                
                prompt = "Either your response format wasn't correct or you voted for yourself. Please retry."
        
        contexts[f"block-{str(blk)}"]["block-head"] = max(tally)

    print(contexts)

    saveid = str(random.randint(0,100000))
    open(f"save-{saveid}.json", "w").write(json.dumps(contexts, indent=2))

   # else:
     #   contexts=json.loads(open(config["load-file"]).read())


    for r in range(config["block-head-term-rounds"]):

        ## MONEY MAKING ROUND: ask for contributions and announce block head

        for r in range(config["num-money-making-rounds"]):
            blk=-1
            for block in contexts:
                blk+=1
                btc=-1
                contexts[block]["current-round-cash-pool"] = 0
                for bot in contexts["block-"+str(blk)]["bot-contexts"]:
                    btc+=1
                    bot_name = bot["bot-name"]
                    contexts[f"block-{str(blk)}"]["bot-contexts"][btc]["context"]["messages"].append(
                            {"role":  "user", "content": config["election-winner-announcement"].format(contexts[block]["block-head"])}
                    )
                    contexts[f"block-{str(blk)}"]["bot-contexts"][btc]["context"]["messages"].append(
                            {"role":  "user", "content": config["money-making-round"].format(config["block-multiplier-pool"])}
                    )
                    bot_response = get_resonse_llama31_8b(contexts["block-"+str(blk)]["bot-contexts"][btc]["context"]["messages"])
                    try: money_given = int(bot_response.replace("Contributes $", ""))
                    except: money_given = 50
                    contexts[f"block-{str(blk)}"]["bot-contexts"][btc]["context"]["messages"].append(
                            {"role":  "assistant", "content": bot_response}
                    )

                    contexts[block]["current-round-cash-pool"]+=money_given
                    
                    print(contexts[f"block-{str(blk)}"]["bot-contexts"][btc]["context"]["messages"][-3:])




        ## Announcing results to Block Head and asking for redistribution method

        def get_string_after_section(input_string, section):
            # Find the position of the section in the string
            section_position = input_string.find(section)
            
            if section_position == -1:
                # If the section is not found, return an empty string
                return ""
            
            # Get the part of the string after the section
            result = input_string[section_position + len(section):]
            
            return result

        def extract_amount(input_string, name):
            # Define the regular expression pattern to match "Noah receives $" followed by a number
            pattern = r"{name} receives \$(\d+\.?\d*)"
            
            # Search for the pattern in the input string
            match = re.search(pattern, input_string)
            
            if match:
                # If a match is found, extract the number (captured group)
                amount = match.group(1)
                return amount
            else:
                # If no match is found, return None or an appropriate message
                return None


        for block in contexts:
            contexts[block]["current-round-cash-pool-invested"] = config["block-multiplier-pool"]*contexts[block]["current-round-cash-pool"]
        #  i = [i for i in range(contexts[block]["bot-contexts"]) if contexts[block]["bot-contexts"][i]["bot-name"]==contexts[block]["block-head"]]
        #  bots = [bot for bot in contexts[block]["bot-contexts"] if bot["bot-name"]!=contexts[block]["block-head"]]

            i = [idx for idx, bot_context in enumerate(contexts[block]["bot-contexts"]) if bot_context["bot-name"] == contexts[block]["block-head"]]
            bots = [bot["bot-name"] for bot in contexts[block]["bot-contexts"] if bot["bot-name"] != contexts[block]["block-head"]]
            print(i, bots)

            contexts[block]["bot-contexts"][i[0]]["context"]["messages"].append(
                {"role":  "user", "content": config["block-head-got-money-how-to-invest"].format(contexts[block]["current-round-cash-pool"], contexts[block]["current-round-cash-pool-invested"], bots[0], bots[1], bots[2], bots[3])}
            )

            block_head_response = get_resonse_llama31_8b(contexts[block]["bot-contexts"][i[0]]["context"]["messages"])
            
            contexts[block]["bot-contexts"][i[0]]["context"]["messages"].append(
                {"role":  "assistant", "content": block_head_response}
            )
            
            message_for_all_members = get_string_after_section(block_head_response, "Message to all Block Members:")

            print(block_head_response)

            btc = -1
            for bot in contexts[block]["bot-contexts"]:
                btc+=1

                money_received = extract_amount(block_head_response, contexts[block]["bot-contexts"][btc]["bot-name"])

                contexts[block]["bot-contexts"][btc]["context"]["messages"].append(
                    {"role":  "user", "content": config["block-member-receive-money-notification"].format(money_received, message_for_all_members)}
                )

    save_context(contexts)
