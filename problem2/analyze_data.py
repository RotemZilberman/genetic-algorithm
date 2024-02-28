import matplotlib.pyplot as plt


def plot_fitness(generation, generation_info, title):
    fig, axis = plt.subplots()
    # iterate over the measures and plot them
    axis.plot(generation, generation_info["best_score"], label='best score', marker='o', color='blue')
    axis.plot(generation, generation_info["avg_score"], label='average score', marker='o', color='red')
    axis.set_xlabel('Generations')
    axis.set_ylabel('fitness score')
    axis.set_title(title)
    axis.legend(loc='center right')
    return fig


def result_to_plot(best_list, avg_eval_list, directory, exp_name):
    info = {"best_score": best_list, "avg_score": avg_eval_list}
    fig = plot_fitness(range(len(best_list)), info, f'Fitness over generations for experience number {exp_name}')
    fig.savefig(f'{directory}/{exp_name}_fitness.png')
