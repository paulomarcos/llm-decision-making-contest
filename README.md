# Battle of the LLM models: Which one is the best at decision-making?
### If you were to choose one model to decide actions for you, which one would you pick?

![](imgs/robots_battling.png)

I let GPT-3.5, GPT-4-turbo and Google Gemini compete at a decision-making contest, and the winner was...
GPT-4! Not such a surprise, but how much was the difference? Did GPT-4 got all the tasks right? How well or poorly did Google's model
achieve? And how was the difference between GPT-4 and GPT-3? We will cover all of these questions, and more, in this article.

> This article has been brought to you by 🐺 [Wolfflow AI](https://wolfflow-ai.com)

Before we go into details, let me contextualize it first.

[In this article](https://medium.com/@paulo_marcos/8-great-time-saving-custom-ai-solutions-with-images-021bf5cd4841), I mentioned 8 examples of custom AI solutions to help businesses improve
their productivity and services, and the last item I added there was **decision-making**.

After writing that article, I wanted to put the LLM models to the test, so that I could
know for sure which model to pick and why. How well would AI be able
to decide which action to take based on a real input?

## What is this battle for?

Imagine we are working with an automation pipeline. This pipeline
consists of an initial message that comes from one of your customers,
and then it is sent automatically to one of your team members: your marketing
manager, your chief engineer, or your secretary. For example, a message requesting
an appointment with you would be sent to your secretary, and not to the other two.

In order for it to be automatically sent to one of these people, the machine
in charge of the automation needs to be able to decide which person to send the message to.

If the machine is not able to pick the right recipient for the message, the
automation pipeline will not make sense. That is how important it is to know
exactly what to expect from LLM models in a decision-making role.

Now with the context clear, let's present the contestants of this battle.

## The contestants

### GPT-3.5
At one side of the ring is GPT-3.5, the model that brought
AI to the real world. Amazing at doing a variety of tasks,
but fall short on more complex ones. Although arguably the weakest contestant,
resource-wise this model is the favorite as the 
cost to run it is the cheapest! 

### GPT-4
At another side of the ring is the evolution of the model above.
GPT-4 brought LLMs to another level and it is the strongest
model released so far. It is the favorite to win the match!

### Gemini
And the last contestant for this battle is the baby Gemini, from
Google. Released last month, it has a lot of potential to tackle
GPT-4 eye-by-eye, but how strong will it be?

## The rules of the battle

Each model will receive a series of text inputs that will be the same
across models, and for each input they will contain the same
set of instructions for the model to base their decision of. Then,
the models will be asked to decide which action to take.

For example, here is a pair of instructions + text input used in the testing:

> Instructions:
>   
> You are a decision-making robot. You will receive a message from the user and decide which method to use based on the user's intention. You will return only an integer that corresponds to that method, and nothing else. Do not answer any questions, do not output anything besides a single integer. Do not engage in conversation. 
The methods are described as follows:
> 
> (1) news: a message containing news from another company, a newsletter or a news website.
> 
> (2) product report: a message detailing metrics, errors, and alerts from cloud applications
> 
> (3) conversation: any message that represents a question or an answer based on a previous email
> 
> (4) others: any other message that is not represented above

And

> Text input:
> 
> Dear David,
> 
> I hope this message finds you well.
> 
> There is an error in the system, would you happen to know the reason for it?
> Please let me know as soon as possible.
>
> 
> Best regards,
> 
> Roger

### Scoring points

Once the model decides which category the input message belongs to,
then we will give one point if it has guessed it right, and no points
if it guessed it wrong.

However, since the model might hallucinate or give any other text
rather than the number of the category, we will penalize that model
by giving a score of -1.

In summary:

- `+1` -> if the model decided correctly
- `0`  -> if the model decided incorrectly
- `-1` -> if the model gives an error or anything other than a single number

## Let the competition begin!

For this battle, I've tested with 17 different texts,
each one belonging to one of the categories mentioned previously: news (1), product report (2), conversation (3), others (4).

![](imgs/first_round.png)

> 👉 [Click here](https://wolfflow-ai.com/llm-decision-making-contest) to view the full sheet with the results and the repository with the code. 

On the first column it is the **ground truth** answer for the text input on the second column.

Then, following that, we have the scores that each of the models received.

Lastly, we have each of the answers given by the models, which was used to give the score on the left.

**For 17 tests, the final score was:**

![](imgs/first_round_results.png)

Yes, Gemini not only didn't guess the right number every time, it also
gave a completely different answer, resulting in -1 scores seventeen times.

So, what the hell happened?

Gemini gave 8 errors out of 17 tries, and guessed numbers 9 times, but these numbers were
negative: -1, -2, -1, -3..., which was not the intended result to get.

For these errors, Gemini's API responded that the text response was not in the right format. 
Digging further, I tried to get the right format to provide the answer, but there was nothing inside
the data to get the answer from. It seems the flag given by the API was "safety issues",
but we can see that by no means the texts had any harm in them.

## GPT-4 Wins! 🏆

StillGPT-4 is the best model to date, and it has proven
in this small trial that it is tough to beat.

One of the mistakes it made was because the text was actually a little ambiguous, so we
can forgive the model for guessing it incorrectly.

The first mistake:

> I hope this email finds you in good health. As the organizer of an upcoming seminar on cutting-edge technologies, I extend an invitation for your participation as a speaker. Your insights would greatly benefit the audience.
> 
> Regards,
> Dr. Carter

GPT model guessed it as being "another message" (number 4), but I labeled it as a normal conversation (3). Interestingly, GPT-3 got this one right!

The second mistake:

> No, I'm about to leave. I'm not sure you will be there, but I hope you will.

Both GPT-4 and GPT-3 got it wrong. Clearly the text is a continuation of some exchange of emails, but both models
decided that it was the category "other" (4). 



## Key takeaways

- GPT-4 model is the best model for decision-making tasks
- GPT-3 is still a good model, but for a real application it lacks the accuracy we need
- Gemini does not work as intended, and even when it does it is not able to make the right decisions
- Changing the instructions, i.e. the prompts, does change the results. So, finding the best one for a specific use-case is necessary

I am also very interested in seeing how other models like LLama-2 and Claude2 perform in this task. 

Get the code [here](https://github.com/paulomarcos/llm-decision-making-contest),
try it with different models and prompts, and let me know the results you get! 


**Enjoyed this article?** I add even more information to help you boost your business with AI in the [Wolfflow AI newsletter](https://wolfflow-ai.beehiiv.com/subscribe)
that gets you articles, tutorials, tools and more straight to your inbox, so that you don't
have to find it every time.

> 👉 [Click here to get effective AI insights into your inbox](https://wolfflow-ai.beehiiv.com/subscribe)


Thank you very much for reading this article and see you next time!