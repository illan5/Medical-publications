# Medical data Assestment

## 1.Analysis
### 1.1 Approach

After a analysis of the document, I used normalization techniques to identify different ways to write the author names. Not all references have the complete first name, for that I took initial letters to create a standardization rule.
On this way we can found collisions, to solve that I could create a class with two attributes, the standardized name and a list of founded versions of the name. I didn't implement this class for not waste a lot of time.

Similar approach with different steps for the institutions.

To improve performance we could use "map-reduce" functions, but not necessary due to the sample volume of data.

### 1.2 Potential failure points

As mentioned in the previous section, with this approach we can have collisions.
In case of high increase of data volume, we could find execution time issues. 
In the most extreme case of high volume we could process in a paralelized way using a spark cluster or AWS Lamdas.

### 1.3 Production

We could deploy this code in AWS Lambdadoind small modifications, triggered by an S3 event when the inputl file comes.
We could also deploy in a linux server and run it from cron or incrontab events.

## 2. Execution
### 2.1 Execution using make

Run 'make' on the root directory

### 2.2 Execute without make

```python
. venv/bin/activate
pip3 install -r requirements.txt --quiet
python3 main.py
```

## 3. Example output

![Example image](https://github.com/illan5/Medical-publications/blob/main/example_medical.png)
