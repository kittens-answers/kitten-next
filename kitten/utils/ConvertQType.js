export default function (qtype) {
  if (qtype === "MATCH") {
    return "Соедините соответствия справа с правильными вариантами";
  } else if (qtype === "MANY") {
    return "Выберите все правильные варианты";
  } else if (qtype === "ORDER") {
    return "Перетащите варианты так, чтобы они оказались в правильном порядке";
  } else if (qtype === "ONE") {
    return "Выберите один правильный вариант";
  } else {
    return "";
  }
}
