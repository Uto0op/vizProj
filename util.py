'''
Utility and reusable functions used across different
pages of the app
'''

import glob
import os
import pandas

# All configuration combinations
algos = ['WAND', 'BMW', 'MaxScore']
orders = ['Random', 'BP']
thresholds = ['None', 'QK', 'Oracle']
rankers = ['BM25', 'BM25-T5', 'DeepImpact']

# Return a list of viable query identifiers
# from the traces directory
def get_querys():
  qfiles = []
  for file in glob.glob("./traces/*.gz"):
    qfiles.append(os.path.basename(file.replace(".gz","")))
  return sorted(qfiles)

# Map algorithm label to data
def get_algo(algo):
  if algo == "WAND":
    return "wand"
  elif algo == "BMW":
    return "block_max_wand"
  elif algo == "MaxScore":
    return "maxscore"
  return "unknown"

# Map order label to data
def get_order(order):
  if order == "Random":
    return "random"
  elif order == "BP":
    return "bp"
  return "unknown"

# Map threshold label to data
def get_threshold(thresh):
  if thresh == "None":
    return "none"
  elif thresh == "QK":
    return "QK"
  elif thresh == "Oracle":
    return "Oracle"
  return "unknown"

# Map ranker label to data
def get_ranker(ranker):
  if ranker == "BM25":
    return "original"
  elif ranker == "BM25-T5":
    return "doct5query"
  elif ranker == "DeepImpact":
    return "deepimpact"
  return "unknown"

# Clean up the stats data frame so it displays nice text
def clean_up_stats_df(df):
  df = df.rename(columns={'ranker': 'Ranker', 
                     'order': 'Order', 
                     'qthresh' : 'Thresh',
                     'algo' : 'Algorithm',
                     'latency' : 'Latency',
                     'docs_scored' : 'Docs Touched',
                     'postings_scored' : 'Postings Scored',
                     'doc_decodes' : 'Doc Blocks Decoded',
                     'freq_decodes' : 'Freq Blocks Decoded'})
  df = df.replace(["wand", "block_max_wand", "maxscore"], 
                  ["WAND", "BMW", "MaxScore"])
  df = df.replace(["original", "doct5query", "deepimpact"], 
                  ["BM25", "BM25-T5", "DeepImpact"])
  df = df.replace("none", "None")
  df = df.replace(["random", "bp"], ["Random", "BP"])
  return df


# Converts query-level metadata to a tuple of strings
def term_data_to_string(term_data):
  items = term_data.split(" ")
  tok_str = ""
  len_str = ""
  ubs_str = ""
  for term in items:
    token,plen,ub = term.split(",")
    tok_str += token + " "
    len_str += plen + " "
    ubs_str += ub + " "
  return (tok_str, len_str, ubs_str)

# Given a query identifier and a ranker,
# grab the statistics and return them
def get_query_info(qid, ranker_type):

    # Get the query data
    df = pandas.read_csv("traces/query-info.txt", sep="\t")
    # Get the desired subsets
    ranker = get_ranker(ranker_type)

    # Subset the data frame
    local_qid = int(qid)
    query_data = df.query("ranker == @ranker and qid == @local_qid")

    # Get the desired data
    qlen = query_data.iloc[0,2]
    term_data = query_data.iloc[0,3]
    tokens, lens, ubs = term_data_to_string(term_data)
    
    # Return it
    return str(local_qid), str(qlen), tokens, lens, ubs

# Given a query identifier, algorithm, ordering, threshold, and ranker,
# get the performance characteristics
def get_performance_info(qid, algo, order, threshold, ranker): 
  # 1. Load the data
    df = clean_up_stats_df(pandas.read_csv("traces/stats.txt", sep=" "))
    qid = int(qid)

    # Subset the data frame
    trace = df.query("Algorithm == @algo and Thresh == @threshold and Ranker == @ranker and Order == @order and qid == @qid")

    # Get the desired data
    latency = trace.iloc[0,8]
    docs_scored = trace.iloc[0,9]
    postings_scored = trace.iloc[0,10]
    dblock_decodes = trace.iloc[0,15]
    fblock_decodes = trace.iloc[0,16]
    return latency, docs_scored, postings_scored, dblock_decodes, fblock_decodes

def stringify(x):
    return "{:,}".format(int(x))

def stringify_list(x):
  try:
    return ["{:,}".format(int(t)) for t in x]
  except:
    return x

