import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class CodeAssistant:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            print("WARNING: No API key found. Running in DEMO mode.\n")
            self.demo_mode = True
        else:
            self.client = OpenAI(api_key=api_key)
            self.model = "gpt-3.5-turbo"
            self.demo_mode = False
    
    def explain_code(self, code):
        if self.demo_mode:
            return f"[DEMO] This code calculates values and processes data. Add your OpenAI API key to .env for real analysis."
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a code explanation expert. Explain code clearly and concisely."},
                {"role": "user", "content": f"Explain this code:\n\n{code}"}
            ]
        )
        return response.choices[0].message.content
    
    def generate_comments(self, code):
        if self.demo_mode:
            lines = code.split('\n')
            commented = []
            for line in lines:
                if line.strip() and not line.strip().startswith('#'):
                    commented.append(f"# Process step")
                commented.append(line)
            return '\n'.join(commented)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Add inline comments to code. Return only the commented code."},
                {"role": "user", "content": f"Add comments to this code:\n\n{code}"}
            ]
        )
        return response.choices[0].message.content
    
    def find_bugs(self, code):
        if self.demo_mode:
            return "[DEMO] Potential issues:\n- Missing error handling\n- No input validation\n\nAdd your OpenAI API key for detailed analysis."
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a bug detection expert. Identify bugs, security issues, and improvements."},
                {"role": "user", "content": f"Find bugs in this code:\n\n{code}"}
            ]
        )
        return response.choices[0].message.content

def main():
    assistant = CodeAssistant()
    
    print("=== AI Code Assistant ===\n")
    print("1. Explain Code")
    print("2. Generate Comments")
    print("3. Find Bugs")
    print("4. Exit\n")
    
    while True:
        choice = input("Choose option (1-4): ")
        
        if choice == "4":
            print("Goodbye!")
            break
        
        if choice in ["1", "2", "3"]:
            print("\nPaste your code (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)
            code = "\n".join(lines[:-1])
            
            if not code.strip():
                print("No code provided.\n")
                continue
            
            print("\nProcessing...\n")
            
            if choice == "1":
                result = assistant.explain_code(code)
            elif choice == "2":
                result = assistant.generate_comments(code)
            else:
                result = assistant.find_bugs(code)
            
            print(f"Result:\n{result}\n")

if __name__ == "__main__":
    main()
