from agents import build_reader_agent, build_serach_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # search agent working
    print("\n" + "=" * 50)
    print("step 1 -- search agent is working ...")
    print("\n" + "=" * 50)

    search_agent = build_serach_agent()
    search_result = search_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Find recent, reliable and detailed information about: {topic}",
                )
            ]
        }
    )

    state["search_results"] = search_result["messages"][-1].content

    print("\n Search result ", state["search_results"])

    print("\n" + "=" * 50)

    print("step 2 -- reader agent is workingggg ...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    try:
        print("Invoking reader...")

        reader_result = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"""
    Based on the following search results about: {topic}

    Search Results:
    {state["search_results"][:800]}
    """,
                    )
                ]
            }
        )

        print("Reader finished!")
        print(reader_result)

    except Exception as e:
        print("Reader error:", repr(e))
    print(reader_result)

    state["scrapped_content"] = reader_result["messages"][-1].content

    print("\n Scrapped content \n", state["scrapped_content"])

    # step 3 - write chain

    print("\n" + "=" * 50)

    print("step 3 -- write chain is workingggg ...")
    print("=" * 50)

    research_combine = (
        f"SEARCH RESULTS: \n {state['search_results']} \n\n"
        f"DEATILED SCRAPED CONTENT: \n {state['scrapped_content']} \n\n"
    )

    state["report"] = writer_chain.invoke(
        {"topic": topic, "research": research_combine}
    )

    print("\n final Research report \n", state["report"])

    # step 4 - Critical chain

    print("\n" + "=" * 50)

    print("step 4 -- Critic is reviewing...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({"report": state["report"]})

    print("\n Critic report \n", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\n Enter research topic :")
    run_research_pipeline(topic=topic)
