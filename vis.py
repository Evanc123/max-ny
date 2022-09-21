import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


leg = pd.read_csv("2022-legislators.csv")

leg["num_introduced"] = (
    leg["num_enacted"]
    + leg["num_needs_signature"]
    + leg["num_in_committee"]
    + leg["num_laid_over"]
    + leg["num_withdrawn"]
)

leg["name"] = leg["name"] + " " + leg["party"] + " " + leg["borough"]

df = leg[
    [
        "name",
        "num_enacted",
        "num_needs_signature",
        "num_in_committee",
        "num_laid_over",
        "num_withdrawn",
    ]
].set_index("name")
df = df.rename(
    {
        "num_enacted": "E",
        "num_needs_signature": "S",
        "num_in_committee": "C",
        "num_laid_over": "O",
        "num_withdrawn": "W",
    },
    axis="columns",
)


fig, axes = plt.subplots(5, 5, figsize=(30, 25))
fig.suptitle("Council Member Legislator Bill Introductions")


for index, grid in enumerate([(x, y) for x in range(0, 5) for y in range(0, 5)]):
    first = df.iloc[index + 26]
    sns.barplot(ax=axes[grid[0], grid[1]], x=first.index, y=first.values)
    axes[grid[0], grid[1]].set_title(first.name)

fig.tight_layout(pad=10.0)
fig.legend(
    [
        "E: Bill Enacted",
        "S: Bill needs Mayoral Signature",
        "C: Bill in Committee",
        "O: Bill Laid Over",
        "W: Bill Withdrawn",
    ],
)

plt.show()
