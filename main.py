# Standard 
# None 

# Pip
# None 

# Custom 
from kindle_extractor import vocab_extractor


if __name__ == "__main__":

    try:
        vocab_extractor()
    except KeyboardInterrupt:
        raise SystemExit("Program exited")
