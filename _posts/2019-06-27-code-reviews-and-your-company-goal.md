---
layout: post
title: "Code Reviews and the Company Goal"
date: 2019-06-27 12:39:52 +0800
---

Code reviews are an important part of how we write code today. It's pretty rare to find a company that doesn't practice code reviews in some shape or form. If the drivers for doing code reviews in the company aren't engineers it's regulation. Code reviews have become a compliance requirement for some security standards (e.g. PCI DSS 3.0)!

The popularity of code reviews is due to the fact that they bring multiple benefits to the engineering process:

1. Ability to catch code defects before the code is shipped to QA or prod.
2. Sharing knowledge with the team.
3. Increase a sense of mutual responsibility.
4. Improve code quality.

Due to all these benefits, we engineers probably all agree that code reviews are necessary to ship stable code to production. But as engineers, we also need to keep in mind how our processes affect our companies. It's important that we ask ourselves how the code review process helps our companies achieve their goal.

## The Goal

According to Eliyahu M. Goldratt and his novel _The Goal_, the goal of most companies is to make money:

> Suddenly it strikes him that the Goal of his company is to make money! Anything that brings him closer to the Goal is productive. Hence, all other activities are non-productive!

Even though The Goal talks about manufacturing and operating a manufacturing plant, most of the ideas apply to other types of processes as well. Read _The Phoneix Project_ to see how _The Goal_ can be applied to IT.

Are code reviews actually a productive activity for the company? As mentioned above, they have a lot of benefits, but they also take precious engineering time away from writing code plus they increase the lead time for new features. Would it be more productive to use that time to write more code instead? The answer to this is no, but only if code reviews are conducted in an efficient manner. When done wrong, even though the intentions were good, they can actually have negative results.

## A bad example

The CTO of Acme inc is obsessed with code quality and sharing knowledge between the engineering team. So much so that the CTO proposes a process that requires every code change to be reviewed by all developers in the engineering department (more than 10 people!).

What are the impacts of this new process to the company?

- This new process will increase code quality as all these reviewers will find more issues with the code than a single or two reviewers ever could. 👍
- This new process will also increase knowledge sharing. Every engineer on the team will see every change going out. 👍
- But this process will make feature velocity grind to a halt. All the engineers will be too busy reviewing all the code! 👎

The company will struggle if releasing new features to the customers will require this many reviews, so even though the intention was a noble one, it will actually hurt the company's goal.

> The road to hell is paved with good intentions.

I have seen a much milder version of this first hand and it wasn't at all obvious that we were doing something counterproductive. We were just focusing on the wrong things when reviewing code, making code reviews too rigid and making the process take too much engineering time without bringing enough value.

So to properly understand how to structure our code review process, let's look at all the main benefits from the list above and see how much value they bring to the company's goal. This will help us figure out what we need to focus on the most when reviewing code.

## 1. Catch code defects before the code is shipped to QA or prod

During my career I have heard the following phrase multiple times:

> Code reviews aren't there to catch bugs, we have the QA team for that.

But if you are looking at code reviews from the standpoint of the value that they bring to the company, detecting issues early is probably the biggest impact that a code review can make. It's definitely the only thing that the users will notice!

Even if you have an amazing QA team that makes sure that bugs don't get deployed to production, there is still the value of finding bugs during the code review process. Fixing the bug found during code review will be much easier and quicker as it will require fewer people to be involved. You might not even need a Jira ticket for it! This will increase your turnaround time and make sure users get your new feature sooner. Quick turnaround time adds value to your company.

Finding bugs is extremely important, but as a reviewer, you also shouldn't spend hours reviewing the code and trying out every edge case by hand. Instead, what you should do is focus on finding bugs when reading through the code as opposed to focusing on styling issues.

Take special care when you see branches in the code path, ask yourself if both branches are covered by tests. Also, pay attention if the author forgot to handle an error case. When you see something that you think _might_ cause a bug, ask the author to write a test to cover that edge case.

According to the company's goal, finding bugs early at the very least allows us to fix defects sooner, allowing us to deploy the new feature to the customers faster. It also helps make sure you don't slip a bug through the cracks and push it to production where it might annoy your users. From this perspective, finding a bug during the code review process is probably the most productive thing that you can do for your company.

## 2. Share knowledge with the team

Every code review is a chance to learn something new. Both for the author of the code and for the reviewers. As a reviewer, you can learn how other people on your team solve problems. As the author, you get feedback on your work which is crucial for self-improvement.

How does sharing knowledge help the goal of your company? It does very little to impact the users directly so this aspect of code reviews is in my opinion not as important as the one described in the previous chapter.

But sharing knowledge still helps your company as it reduces the bus factor - the measurement of the risk resulting from information and capabilities not being shared among team members. It also integrates learning and self-improvement into your engineering process which is crucial for your company to grow.

So make sure you look for ways to share knowledge when doing code reviews, but only after you are sure that you can't find any defects with the code.

## 3. Increase a sense of mutual responsibility

Your whole team needs to own their code collectivity. If a single person is responsible for a part of the system it's a risk for your business as that person will be the bottleneck for every new feature that touches that part of the system. Bottlenecks like this can bring your feature velocity to a standstill, so it's always a good idea to see if you can reduce them.

This doesn't directly impact the company's goal, but it can still have a huge impact indirectly. Make sure that you share as much knowledge as possible during the code review process to avoid bottlenecks like the one described above.

## 4. Improve code quality

Code reviews are a good way to catch little improvements to the code. It feels great when you point out that a few lines of code can be deleted because there is already an existing function that does the same thing.

But be careful, being overly pedantic about every little style issue can have negative impacts on the productivity of your team!

I have seen requesting a whitespace delay the new feature from shipping for a few weeks because the change request made it miss the release window. Be mindful of how much company value is gained by making code style comments and perhaps rather invest some time to automate this into your test suite or the use of an autoformatter.

Try to make sure code style issues are detected automatically, without human interaction. After that only mention styling issues only when there are no bugs to point out or there is no way to share knowledge. And if the reviewer doesn't agree with the change, don't persist.

## Conclusion

Be mindful of the company goal when doing code reviews. Ask yourself how much value your code review comment brings to the table. If you are asking to change some whitespace, the value will be very small. If you are asking to change the code that might misbehave under certain conditions exposing sensitive customer data, the value will be huge.

When doing code reviews, try to write more comments with a higher value than lower value.

Learned something new? Be sure to share what you've learned with your team. Sharing knowledge is one of the most important parts of your job 😉

In the next blog post, I'll talk about how to make sure code reviews have as little impact on feature velocity as possible. Sign up below to get the article in your inbox as soon as it's ready.
