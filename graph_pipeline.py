from langgraph.graph import StateGraph, END

# Define the "State" that flows through the graph
class CryptoState(dict):
    pass


# ---- Your tasks (functions) ----
def ingest_task(state: CryptoState):
    print("Running ingest...")
    state["prices"] = "fetched price data"
    return state

def compute_features(state: CryptoState):
    print("Computing features...")
    state["features"] = "computed technical indicators"
    return state

def forecast_task(state: CryptoState):
    print("Running forecasting...")
    state["forecast"] = "7-day prediction"
    return state

def sentiment_task(state: CryptoState):
    print("Running sentiment...")
    state["sentiment"] = "sentiment score"
    return state

def compose_report(state: CryptoState):
    print("Composing report...")
    state["report"] = "Final market report"
    return state


# ---- Build LangGraph using modern API ----
graph = StateGraph(CryptoState)

# Add nodes
graph.add_node("ingest", ingest_task)
graph.add_node("features", compute_features)
graph.add_node("forecast", forecast_task)
graph.add_node("sentiment", sentiment_task)
graph.add_node("report", compose_report)

# Set entry point
graph.set_entry_point("ingest")

# Add edges (dependencies)
graph.add_edge("ingest", "features")
graph.add_edge("features", "forecast")
graph.add_edge("ingest", "sentiment")
graph.add_edge("forecast", "report")
graph.add_edge("sentiment", "report")
graph.add_edge("report", END)

# Compile the graph
app = graph.compile()

# ---- Run the graph ----
result = app.invoke({})
print("\nFINAL OUTPUT:")
print(result)


