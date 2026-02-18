from langchain_core.tools import tool

@tool
def summary(
  farewell: str,
  level: str,
  successes: str,
  mistakes: str,
  soft: str,
  roadmap: str
  ):
  """Воспользуйся этим инструментом, чтобы показать пользователю финальный вердикт."""
  print(farewell)
  final_feedback = f"""
  Уровень: {level};
  Хорошие стороны: {successes};
  Плохие стороны: {mistakes};
  Soft skills: {soft};
  Roadmap: {roadmap}
  """
  print(f"Вот финальный вердикт по твоему выступлению:\n{final_feedback}")
  return final_feedback


tools = [summary]
