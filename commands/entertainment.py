"""
Enhanced Entertainment Commands
Handles jokes, facts, fun interactions, and engaging activities
"""
import random
from typing import List, Dict, Any
from logger import logger

class EntertainmentCommands:
    """Handles entertainment-related commands with enhanced engagement"""
    
    @staticmethod
    def get_random_joke() -> str:
        """Return a random joke with enhanced delivery"""
        jokes = [
            ("Why don't scientists trust atoms? Because they make up everything!", "Haha! Get it? Atoms make up everything!"),
            ("What did one ocean say to the other ocean? Nothing, they just waved!", "Ocean humor is always a wave!"),
            ("Why did the scarecrow win an award? He was outstanding in his field!", "That scarecrow really knows how to stand out!"),
            ("I'm reading a book about anti-gravity. It's impossible to put down!", "I couldn't put it down either!"),
            ("Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!", "Math jokes are always number one!"),
            ("Why don't eggs tell jokes? They'd crack each other up!", "Egg-cellent humor!"),
            ("I wondered why the baseball kept getting bigger. Then it hit me!", "That's a real curveball of a joke!"),
            ("What do you call a fake noodle? An impasta!", "That's pasta-bly the best joke ever!"),
            ("How does a penguin build its house? Igloos it together!", "That's ice cold humor!"),
            ("Why did the bicycle fall over? Because it was two tired!", "That bike really needed a rest!"),
            ("What do you call a bear with no teeth? A gummy bear!", "That's un-bear-ably cute!"),
            ("Why don't skeletons fight each other? They don't have the guts!", "That's bone-chilling humor!"),
            ("What's orange and sounds like a parrot? A carrot!", "That's a real head-scratcher!"),
            ("Why did the math book look sad? Because it had too many problems!", "Math books always have too many issues!"),
            ("What do you call a sleeping bull? A bulldozer!", "That's a heavy sleeper!"),
            ("Why did the cookie go to the doctor? Because it was feeling crummy!", "That's a sweet joke!"),
            ("What do you call a fish without eyes? A fsh!", "That's fin-tastic humor!"),
            ("Why did the student eat his homework? Because the teacher told him it was a piece of cake!", "Homework never tasted so good!")
        ]
        
        joke, punchline = random.choice(jokes)
        logger.info("Joke provided")
        return f"{joke} {punchline}"
    
    @staticmethod
    def get_random_fact() -> str:
        """Return a random interesting fact with engaging delivery"""
        facts = [
            ("Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat.", "That's sweet news!"),
            ("Octopuses have three hearts and blue blood.", "How cool is that! They're truly unique!"),
            ("A group of flamingos is called a 'flamboyance'.", "That's so fancy! I love it!"),
            ("The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.", "That was quick!"),
            ("The inventor of the frisbee was turned into a frisbee after he died.", "Now that's going out with a spin!"),
            ("Bananas are berries, but strawberries aren't.", "Mind blown! Nature is weird!"),
            ("A day on Venus is longer than a year on Venus.", "Time works differently there!"),
            ("The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion.", "It grows in the heat!"),
            ("Cows have best friends and get stressed when they're separated.", "That's so adorable! Cow friendships are real!"),
            ("The dot over the letter 'i' is called a tittle.", "I never knew that! So tiny and cute!"),
            ("A single cloud can weigh more than a million pounds.", "That's heavy! Clouds are heavier than they look!"),
            ("The human brain uses about 20% of the body's total energy.", "Our brains are energy hungry!"),
            ("A group of unicorns is called a blessing.", "That's magical! I love that!"),
            ("The heart of a shrimp is located in its head.", "Shrimp are so interesting!"),
            ("A strawberry isn't a berry, but a banana is.", "Nature likes to surprise us!"),
            ("Water makes a unique sound when it freezes, and scientists call it the 'ice quack'.", "Even ice likes to make noise!"),
            ("The inventor of the Pringles can is buried in one.", "Now that's dedication to your invention!"),
            ("A jiffy is an actual unit of time: 1/100th of a second.", "I'll be back in a jiffy!"),
            ("The unicorn is Scotland's national animal.", "Scotland knows what's magical!"),
            ("Honeybees can recognize human faces.", "They're smarter than we think!")
        ]
        
        fact, comment = random.choice(facts)
        logger.info("Fact provided")
        return f"{fact} {comment}"
    
    @staticmethod
    def get_random_compliment() -> str:
        """Return a random compliment to brighten someone's day"""
        compliments = [
            "You're doing an amazing job just by being yourself!",
            "Your curiosity makes the world a more interesting place!",
            "You have such a wonderful way of seeing things!",
            "The world is better with you in it!",
            "You're braver than you believe, stronger than you seem, and smarter than you think!",
            "Your smile could light up a whole room!",
            "You have the power to make someone's day brighter!",
            "You're like a human sunshine!",
            "Your kindness ripples out and touches everyone around you!",
            "You make the world a more beautiful place just by being you!",
            "Your enthusiasm is contagious!",
            "You have such a wonderful heart!",
            "You're one in a million!",
            "Your potential is limitless!",
            "You're doing great, and I'm proud of you!"
        ]
        return random.choice(compliments)
    
    @staticmethod
    def get_random_quote() -> str:
        """Return an inspiring quote"""
        quotes = [
            ("The only way to do great work is to love what you do.", "Steve Jobs"),
            ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
            ("Life is what happens when you're busy making other plans.", "John Lennon"),
            ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
            ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
            ("Everything you can imagine is real.", "Pablo Picasso"),
            ("Do what you can, with what you have, where you are.", "Theodore Roosevelt"),
            ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
            ("You are never too old to set another goal or to dream a new dream.", "C.S. Lewis"),
            ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
            ("Your time is limited, don't waste it living someone else's life.", "Steve Jobs"),
            ("If you look at what you have in life, you'll always have more.", "Oprah Winfrey"),
            ("If you set your goals ridiculously high and it's a failure, you will fail above everyone else's success.", "James Cameron"),
            ("Life is either a daring adventure or nothing at all.", "Helen Keller"),
            ("The purpose of our lives is to be happy.", "Dalai Lama")
        ]
        
        quote, author = random.choice(quotes)
        return f'"{quote}" - {author}'
    
    @staticmethod
    def get_word_of_the_day() -> str:
        """Return an interesting word with its meaning"""
        words = [
            {"word": "Ephemeral", "meaning": "lasting for a very short time", "example": "The ephemeral beauty of cherry blossoms makes them even more special."},
            {"word": "Serendipity", "meaning": "finding good things by chance", "example": "Finding that book was pure serendipity!"},
            {"word": "Wanderlust", "meaning": "a strong desire to travel", "example": "My wanderlust always makes me dream of faraway places."},
            {"word": "Eunoia", "meaning": "beautiful thinking; a calm mind", "example": "Meditation helps me achieve eunoia."},
            {"word": "Petrichor", "meaning": "the pleasant smell after rain", "example": "I love the petrichor after a summer rain."},
            {"word": "Sonder", "meaning": "realizing each stranger has a life as complex as yours", "example": "Walking through the city, I felt a deep sense of sonder."},
            {"word": "Aurora", "meaning": "dawn; also the natural light display in the sky", "example": "The northern lights are a spectacular aurora."},
            {"word": "Luminescence", "meaning": "light emitted without heat", "example": "Fireflies produce a beautiful luminescence."},
            {"word": "Ethereal", "meaning": "extremely delicate and light", "example": "Her voice had an ethereal quality to it."},
            {"word": "Ineffable", "meaning": "too great to be expressed in words", "example": "The beauty of the sunset was ineffable."}
        ]
        
        word_data = random.choice(words)
        return f"Today's word is '{word_data['word']}'. It means {word_data['meaning']}. For example: {word_data['example']}"
    
    @staticmethod
    def get_thought_of_the_day() -> str:
        """Return a thoughtful question or reflection"""
        thoughts = [
            "If you could have dinner with any person, living or dead, who would it be?",
            "What's the most beautiful place you've ever been to?",
            "If you could learn any skill instantly, what would it be?",
            "What's something that always makes you smile?",
            "If you could travel anywhere tomorrow, where would you go?",
            "What's the best advice you've ever received?",
            "If you could have any superpower, what would you choose?",
            "What's something you're really proud of?",
            "If you could relive one day of your life, which would it be?",
            "What's the kindest thing anyone has ever done for you?",
            "If you could solve one world problem, what would it be?",
            "What's your favorite memory from childhood?",
            "If you could master any language, which would you choose?",
            "What's something you've always wanted to try?",
            "If you could give your younger self one piece of advice, what would it be?"
        ]
        return random.choice(thoughts)
    
    @staticmethod
    def calculate(expression: str) -> str:
        """Perform basic calculations safely with friendly output"""
        try:
            # Remove spaces and validate expression
            import re
            clean_expr = re.sub(r'\s+', '', expression)
            
            # Only allow safe mathematical operations and numbers
            allowed_pattern = r'^[0-9+\-*/().%]+$'
            if not re.match(allowed_pattern, clean_expr):
                return "Oops! I can only calculate with numbers and basic operators (+, -, *, /, %, (), .). Try something like '2 + 2' or '10 * 5'!"
            
            # Use ast.literal_eval for safer evaluation
            import ast
            import operator
            
            # Define safe operations
            ops = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Mod: operator.mod,
                ast.USub: operator.neg,
            }
            
            def eval_expr(node):
                if isinstance(node, ast.Num):  # <number>
                    return node.n
                elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                    return ops[type(node.op)](eval_expr(node.left), eval_expr(node.right))
                elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
                    return ops[type(node.op)](eval_expr(node.operand))
                else:
                    raise TypeError(node)
            
            result = eval_expr(ast.parse(clean_expr, mode='eval').body)
            
            # Format the result nicely
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            logger.info(f"Calculation performed: {expression} = {result}")
            return f"The answer is {result}! Math is fun!"
            
        except Exception as e:
            logger.error(f"Calculation error: {e}")
            return f"Oops! I had a little trouble with that calculation. Could you try rephrasing it? Maybe something like '15 + 25' or '100 divided by 4'?"
