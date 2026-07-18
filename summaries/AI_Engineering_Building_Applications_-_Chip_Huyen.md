# AI Engineering: Building Applications with Foundation Models - Chip Huyen

## Comprehensive Summary

---

## Part I: Foundations

### Chapter 1: When to Build AI Applications

Before building an AI application, ask three questions:
1. **Is this application necessary?** Many "AI problems" are better solved with traditional software. If a heuristic, rules engine, or simple lookup table works, use it. AI adds complexity, cost, and unpredictability.
2. **Is AI needed?** AI is justified when the problem involves ambiguity, pattern recognition, or generating content at scale. Traditional ML suffices for structured prediction tasks.
3. **Do I have to build it myself?** Before custom development, consider: using existing APIs (OpenAI, Anthropic, Google), buying off-the-shelf solutions, or fine-tuning existing models.

**Successful use cases for foundation models:**
- **Content generation**: Code, marketing copy, documentation, emails
- **Summarization**: Meeting notes, long documents, research papers
- **Search and retrieval**: Semantic search over enterprise documents
- **Conversation**: Customer support bots, tutoring systems, therapy assistants
- **Translation and localization**: Real-time translation across languages
- **Data extraction**: Pulling structured data from unstructured documents
- **Code assistance**: Autocomplete, code review, debugging
- **Classification and routing**: Intent detection, sentiment analysis, spam filtering

**Traditional ML Engineering vs. AI Engineering:**

| Aspect | Traditional ML | AI Engineering (Foundation Models) |
|--------|---------------|-----------------------------------|
| Data | Tabular, structured | Text, images, multimodal |
| Features | Manual feature engineering | Learned from data |
| Training | Train from scratch | Fine-tune or prompt |
| Evaluation | Clear metrics | Nuanced, harder to define |
| Deployment | Model-specific infrastructure | API calls or model hosting |
| Cost | Compute for training | API costs, inference compute |

### Chapter 2: Understanding Foundation Models

**What makes a foundation model:**
- **Training data recipe**: Massive web crawls (Common Crawl, The Pile), curated datasets, code repositories, books, scientific papers. Data quality matters more than quantity. Data deduplication and filtering are critical.
- **Architecture**: Transformers with self-attention mechanism. Key innovations: multi-head attention, positional encoding, layer normalization. Decoder-only architectures (GPT family) predict next tokens; encoder-decoder architectures (T5) understand bidirectional context.
- **Scale**: Parameter counts from 1B to 1T+. Training requires thousands of GPUs, months of compute. Scaling laws (Chinchilla paper) show that model quality improves predictably with more parameters and more data.
- **Training stages**:
  1. **Pre-training**: Next-token prediction on massive data. Creates base capabilities.
  2. **Supervised Fine-Tuning (SFT)**: Training on high-quality instruction-response pairs. Teaches the model to follow instructions.
  3. **Reinforcement Learning from Human Feedback (RLHF)**: Training with a reward model based on human preferences. Aligns model outputs with human values and preferences.
  4. **Direct Preference Optimization (DPO)**: A simpler alternative to RLHF that directly optimizes for preferred outputs.

**How models generate responses:**
- **Tokenization**: Text is split into tokens (subwords). The model operates on token IDs.
- **Autoregressive generation**: Each token is predicted based on all previous tokens. The model outputs a probability distribution over the vocabulary for the next token.
- **Sampling strategies**:
  - **Greedy**: Always pick the highest probability token. Deterministic but repetitive.
  - **Top-k**: Sample from the k most likely tokens. Adds variety.
  - **Top-p (nucleus sampling)**: Sample from the smallest set of tokens whose cumulative probability exceeds p. More adaptive than top-k.
  - **Temperature**: Controls randomness. Low temperature (0.1) = more deterministic; high temperature (1.0+) = more random. Temperature 0 is greedy.
  - **Beam search**: Explore multiple sequences simultaneously. Used for tasks requiring more deterministic outputs.

**Why models hallucinate:**
Hallucinations have multiple root causes:
1. **Training data issues**: Models memorize incorrect information from noisy training data
2. **Next-token prediction limitation**: The model predicts plausible-sounding tokens, not necessarily truthful ones. It optimizes for fluency over factuality.
3. **Snowballing hallucinations**: An initial incorrect assumption leads the model to generate increasingly incorrect follow-up content to remain consistent with the initial error
4. **Knowledge-labeler mismatch**: During SFT, labelers write responses using their knowledge, but the model may not share that knowledge, teaching it to fabricate plausible answers
5. **Lack of uncertainty awareness**: Models don't inherently know what they don't know

**Mitigation strategies:**
- Ground responses in retrieved documents (RAG)
- Instruct the model to say "I don't know" when uncertain
- Use lower temperature settings
- Fact-checking pipelines
- Post-generation verification

---

## Part II: Evaluation

### Chapter 3: Evaluation Methods

Evaluation is the hardest challenge in AI engineering. Without rigorous evaluation, you can't tell if changes improve or hurt your application.

**Types of evaluation:**

1. **Exact evaluation**: Compare output to a gold-standard answer. Works for classification, extraction, structured tasks.
   - Metrics: Exact match, F1, accuracy
   - Tools: String matching, regex

2. **LLM-as-judge**: Use a stronger model to evaluate outputs of a weaker model.
   - Advantages: Scalable, cheap, consistent
   - Risks: Judge model has its own biases, may prefer verbose outputs, may align with its own style
   - Best practices: Use pairwise comparison, clear rubrics, multiple judges, calibrate against human evaluation

3. **Human evaluation**: Gold standard but expensive and slow.
   - Use for high-stakes decisions, edge cases, and calibrating automated metrics
   - Inter-annotator agreement (Cohen's kappa) measures consistency

4. **Embedding-based evaluation**: Convert outputs to embeddings and measure similarity to reference answers using cosine similarity or other distance metrics.

**Evaluation pipeline design:**

Step 1: **Tie evaluation metrics to business metrics.** A translation app's evaluation should measure translation quality (BLEU, COMET), not just fluency.

Step 2: **Define evaluation criteria.** What makes a good output? Create scoring rubrics with examples:
- Correctness: Is the information accurate?
- Relevance: Does it address the question?
- Completeness: Does it cover all aspects?
- Clarity: Is the output well-organized?
- Safety: Does it avoid harmful content?

Step 3: **Create evaluation data.** Curate a representative dataset. Include:
- Typical cases (most common queries)
- Edge cases (unusual inputs)
- Adversarial cases (inputs designed to break the system)
- Regression cases (previously fixed bugs)

Step 4: **Choose evaluation methods.** Combine automated and human evaluation.

Step 5: **Iterate.** Your evaluation pipeline should evolve with your application.

### Chapter 4: Evaluation in Practice

**Evaluating specific components:**

- **Retrieval evaluation**: Measure precision, recall, MRR, NDCG of retrieved documents
- **Generation evaluation**: Measure faithfulness (does the output follow retrieved context?), relevance, coherence
- **End-to-end evaluation**: Measure user satisfaction, task completion rate

**Public benchmarks:**
- MMLU, HumanEval, GSM8K, MATH for general capability
- TruthfulQA for factuality
- HELM for holistic evaluation
- Chatbot Arena for human preference ranking

**Benchmarks have limitations:**
- Data contamination (test data leaks into training data)
- Narrow task coverage
- Static snapshots that don't represent real usage
- Goodhart's law: optimizing for benchmarks doesn't guarantee real-world quality

**Building your own evaluation:**
Start with public benchmarks for model selection, but invest in building domain-specific evaluation datasets that reflect your actual use cases.

---

## Part III: Building AI Applications

### Chapter 5: Prompt Engineering

Prompt engineering is the first optimization lever, and it should be exhausted before considering more expensive approaches like fine-tuning.

**Core principles:**
1. **Be specific and detailed**: Vague prompts produce vague outputs. Specify format, length, tone, audience.
2. **Provide examples (few-shot prompting)**: Include 2-5 examples of input-output pairs to demonstrate the desired behavior.
3. **Use structured prompts**: System prompt + user prompt + assistant context.

**Advanced techniques:**

- **Chain-of-Thought (CoT)**: Ask the model to reason step-by-step. Dramatically improves performance on reasoning tasks. "Let's think step by step" can unlock better performance.
- **Self-consistency**: Generate multiple chain-of-thought responses and take the majority answer. Reduces errors from any single reasoning path.
- **Tree-of-Thought (ToT)**: Explore multiple reasoning paths simultaneously, evaluate each, and backtrack from dead ends. Good for complex planning tasks.
- **ReAct (Reasoning + Acting)**: Interleave reasoning steps with tool use. The model reasons about what action to take, takes the action, observes the result, and continues reasoning.
- **Meta-prompting**: Use one prompt to generate or optimize another prompt.

**Prompt design patterns:**
- **Role-playing**: "You are an expert software engineer..."
- **Output formatting**: "Respond in JSON with keys: {name, age, role}"
- **Constraint specification**: "Do not use information outside the provided context"
- **Verification**: "Double-check your answer before responding"
- **Decomposition**: Break complex tasks into smaller sub-tasks

**Prompt engineering limitations:**
- Prompt length is limited by context window
- Complex prompts can confuse the model
- Results are non-deterministic (same prompt, different outputs)
- Prompt engineering alone can't teach the model new knowledge

### Chapter 6: RAG and Agents

#### Retrieval-Augmented Generation (RAG)

RAG addresses two fundamental limitations of foundation models: knowledge cutoff (models don't know recent events) and hallucination (models fabricate information).

**How RAG works:**
1. **Indexing**: Documents are chunked, converted to embeddings, and stored in a vector database
2. **Retrieval**: Given a query, find the most relevant chunks using similarity search
3. **Generation**: Feed retrieved chunks as context to the model along with the query

**Chunking strategies:**
- **Fixed-size chunks**: Simple but may break semantic coherence
- **Sentence-based chunks**: Better coherence but variable sizes
- **Semantic chunking**: Split at topic boundaries using embeddings
- **Recursive chunking**: Hierarchical approach with overlap

**Retrieval strategies:**
- **Dense retrieval**: Vector similarity search using embeddings
- **Sparse retrieval**: BM25, TF-IDF keyword matching
- **Hybrid retrieval**: Combine dense and sparse for better recall
- **Re-ranking**: Use a cross-encoder to re-rank retrieved documents for precision
- **Query transformation**: Rewrite or expand queries for better retrieval

**Advanced RAG patterns:**
- **Multi-hop RAG**: Retrieve iteratively, using previous results to inform next queries
- **Self-RAG**: Model decides when to retrieve and when to answer from its own knowledge
- **Agentic RAG**: Use an agent to plan retrieval, evaluate results, and decide next steps

#### Agents

An AI agent is a system that can perceive its environment, reason about goals, and take actions to achieve those goals.

**Agent components:**
1. **Planning**: Break goals into actionable steps
2. **Memory**: Store and retrieve information across interactions
   - Short-term memory: Current conversation context
   - Long-term memory: Persisted knowledge (vector store, database)
   - Working memory: Information actively being used
3. **Tools**: External capabilities the agent can invoke
   - Function calling / tool use
   - API integrations
   - Code execution
   - Web browsing
4. **Action**: Execute planned steps using tools

**Agent architectures:**
- **Single-agent**: One model handles planning and execution
- **Multi-agent**: Multiple specialized agents collaborate
  - Supervisor pattern: One agent orchestrates others
  - Peer pattern: Agents communicate directly
  - Hierarchical: Agents organized in a tree structure

**Memory hierarchy for agents:**
- Internal knowledge (model weights) → always available, expensive to update
- Short-term memory (context window) → current session, limited capacity
- Long-term memory (external storage) → persistent, cheap to update

**Evaluating agents:**
- Task completion rate
- Number of steps to complete a task
- Tool usage accuracy
- Cost per task (API calls, tokens)
- Ability to recover from errors

### Chapter 7: Fine-Tuning

Fine-tuning adapts a pre-trained model to specific tasks or domains. It should be considered after prompt engineering and RAG have been exhausted.

**When to fine-tune:**
- You need consistent output format
- The domain has specialized vocabulary or knowledge
- You need the model to learn specific patterns (e.g., company-specific responses)
- Latency is critical and you need a smaller model to perform well

**When NOT to fine-tune:**
- You just need to add new knowledge (use RAG instead)
- You have very little training data
- The task changes frequently
- You can achieve good results with prompting

**Parameter-efficient fine-tuning (PEFT):**
- **LoRA (Low-Rank Adaptation)**: Add small trainable rank decomposition matrices to each layer. Only ~1% of parameters are trained, but performance is close to full fine-tuning.
- **QLoRA**: LoRA with quantized base model. Even more memory efficient.
- **Adapter layers**: Insert small trainable modules between transformer layers.
- **Prefix tuning**: Train a small number of virtual tokens prepended to the input.

**Fine-tuning data:**
- Quality matters far more than quantity. 1,000 high-quality examples can outperform 100,000 mediocre ones.
- Data should be representative of production distribution
- Include diverse examples covering edge cases
- Validate data quality with human review
- Synthetic data from stronger models can supplement real data

**Supervised Fine-Tuning (SFT) process:**
1. Collect high-quality input-output pairs
2. Format into instruction-response pairs
3. Train the model to minimize the loss between its outputs and the reference outputs
4. Evaluate on held-out data

### Chapter 8: Dataset Engineering

The quality of your AI application is bounded by the quality of your data.

**Data flywheel:**
1. Deploy model → Users interact → Collect data → Label/filter data → Train model → Deploy improved model
2. The more users you have, the more data you collect, the better your model gets

**Data collection strategies:**
- Production traffic sampling
- Synthetic data generation using stronger models
- Public datasets and benchmarks
- Human annotation services

**Data quality:**
- **Accuracy**: Labels are correct
- **Coverage**: Dataset covers the full distribution of production inputs
- **Diversity**: No bias toward specific patterns
- **Timeliness**: Data reflects current conditions

**Annotation best practices:**
- Write clear annotation guidelines with examples
- Use multiple annotators and measure inter-annotator agreement
- Iterate on guidelines based on disagreement patterns
- Invest in tooling for efficient annotation

**Synthetic data:**
- Use stronger models (e.g., GPT-4) to generate training data for smaller models
- Validate synthetic data quality before using it for training
- Watch for model collapse (training on model outputs degrades quality over generations)

### Chapter 9: Model Selection and Serving

**Model selection criteria:**
1. **Quality**: Performance on your specific task
2. **Latency**: Time to first token and tokens per second
3. **Cost**: Per-token pricing or hosting costs
4. **Context window**: Maximum input + output length
5. **Capabilities**: Tool use, structured output, multimodal support
6. **Privacy**: Can you use external APIs or must you self-host?

**Model hosting options:**
- **API providers**: OpenAI, Anthropic, Google, Cohere, Mistral. Easiest, but vendor lock-in and data privacy concerns.
- **Cloud-hosted**: Deploy open-source models on AWS, GCP, Azure. More control, moderate complexity.
- **Self-hosted**: Run models on your own infrastructure. Maximum control, highest complexity.

**Inference optimization:**

1. **Quantization**: Reduce model precision (FP16 → INT8 → INT4). Smaller model, faster inference, slight quality loss.
   - Post-training quantization (PTQ): Quantize after training
   - Quantization-aware training (QAT): Train with quantization in mind

2. **Distillation**: Train a smaller "student" model to mimic a larger "teacher" model. The student is faster and cheaper while retaining much of the teacher's capability.

3. **Pruning**: Remove less important weights from the model. Structured pruning removes entire neurons/heads; unstructured pruning removes individual weights.

4. **Speculative decoding**: Use a small draft model to generate candidate tokens, then verify with the large model in parallel. Speeds up autoregressive generation.

5. **KV cache optimization**: Cache key-value pairs from previous tokens to avoid recomputation. PagedAttention manages KV cache memory more efficiently.

6. **Batching**: Group multiple requests together for efficient GPU utilization. Continuous batching dynamically adds and removes requests from the batch.

**Serving infrastructure:**
- Load balancing across model replicas
- Autoscaling based on request volume
- Caching for common queries
- Rate limiting and authentication
- Monitoring and observability

### Chapter 10: Security and Safety

**Security threats:**

1. **Prompt injection**: Malicious instructions embedded in user input that override the system prompt
   - Direct injection: User explicitly provides override instructions
   - Indirect injection: Malicious instructions embedded in retrieved documents or external data
   - Defenses: Input sanitization, separate system/user context, output monitoring

2. **Data poisoning**: Adversaries corrupt training or fine-tuning data to introduce backdoors or biases

3. **Model extraction**: Attackers query the model extensively to create a copy

4. **Privacy leakage**: Models may memorize and reproduce sensitive training data
   - Training data extraction attacks
   - Membership inference attacks (determine if specific data was in training set)

5. **Supply chain attacks**: Compromised models, frameworks, or dependencies

**Safety considerations:**

- **Content moderation**: Filter harmful outputs. Use separate classification models or the model itself with safety prompts.
- **Bias and fairness**: Audit outputs for demographic biases. Use diverse evaluation data.
- **Misuse prevention**: Rate limit capabilities that could be misused. Implement usage policies.
- **Transparency**: Be clear with users about AI-generated content. Provide citations when possible.

**Responsible AI practices:**
- Red-teaming: Actively try to break your system before deployment
- Gradual rollout: Deploy to small groups first, monitor, then expand
- Feedback mechanisms: Let users report problems
- Incident response: Have a plan for when things go wrong

---

## Part IV: Building Production Systems

### The AI Engineering Lifecycle

1. **Problem framing**: Define the problem, determine if AI is the right solution
2. **Model selection**: Evaluate and select foundation models
3. **Prompt engineering**: Optimize prompts for your use case
4. **RAG pipeline**: Build retrieval and generation pipeline
5. **Evaluation**: Create evaluation benchmarks and metrics
6. **Fine-tuning** (if needed): Adapt model to your domain
7. **Deployment**: Set up serving infrastructure
8. **Monitoring**: Track quality, latency, cost, safety
9. **Iteration**: Continuous improvement based on user feedback

### Key Takeaways

1. **Start simple**: Begin with prompting, then RAG, then fine-tuning. Each step adds complexity and cost.
2. **Evaluation is paramount**: You can't improve what you can't measure. Invest heavily in evaluation infrastructure.
3. **Data quality over quantity**: A small set of high-quality examples outperforms massive low-quality datasets.
4. **Optimize for the bottleneck**: Profile your application to determine if quality, latency, or cost is the bottleneck, then address that specifically.
5. **Build for iteration**: AI applications require continuous improvement. Design your system for easy experimentation and deployment.
6. **Safety is non-negotiable**: Plan for adversarial inputs, bias, and misuse from day one.
7. **The field moves fast**: Foundation models improve rapidly. Design your system to be model-agnostic so you can swap models as better ones become available.
8. **RAG is usually sufficient**: Most applications don't need fine-tuning. A well-designed RAG pipeline with good prompting solves most problems.
9. **Cost matters at scale**: A 2x cost difference per token becomes millions of dollars at scale. Optimize inference.
10. **Human oversight remains essential**: AI systems should augment human decision-making, not replace it for high-stakes decisions.
