def rand_draw(rng, n_list, q_list):
  chosen_name = rng.choice(n_list)
  chosen_question = rng.choice(q_list)

  return (chosen_name, chosen_question)


def pick_excluding(rng, items, exclude):
  """Pick a random item not in exclude; auto-reset (ignore exclude) once every item has been used."""
  candidates = [item for item in items if item not in exclude]
  if not candidates:
    candidates = list(items)
  if not candidates:
    return None
  return rng.choice(candidates)


def rand_draw_no_repeat(rng, n_list, q_list, used_names, used_questions):
  chosen_name = pick_excluding(rng, n_list, used_names)
  chosen_question = pick_excluding(rng, q_list, used_questions)

  return (chosen_name, chosen_question)