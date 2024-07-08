# Ollama Cog Model - llama3:8b

This is an implementation of the Ollama model [llama3:8b](https://ollama.com/library/llama3:8b) as a [Cog](https://github.com/replicate/cog) model.

## Development

Follow the [model pushing guide](https://replicate.com/docs/guides/push-a-model) to push your own model to [Replicate](https://replicate.com).

## Deploy

Clone this repo, and then run:
    
    cog push
    
## Basic Usage

To run a prediction:

    cog predict -i prompt="tell me a joke"


## Output

    Why couldn't the bicycle stand up by itself?

    (Wait for it...)

    Because it was two-tired!



