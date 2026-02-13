let palavraAtual = "";

function carregarProgresso() {
  fetch("/progresso")
    .then(res => res.json())
    .then(data => {
      atualizarTela(data.etapa, data.total);
    });
}

function atualizarTela(etapa, total) {
  fetch("/progresso")
    .then(res => res.json())
    .then(data => {
      palavraAtual = null;
    });

  fetch("/verificar", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({resposta: ""})
  });

  fetch("/progresso")
    .then(res => res.json())
    .then(data => {
      if (data.etapa >= data.total) {
        document.getElementById("titulo").innerText = "🎉 Concluído!";
        document.getElementById("palavra").innerText = "";
      } else {
        fetch("/verificar", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({resposta: "skip"})
        });

        palavraAtual = data.etapa;
        document.getElementById("titulo").innerText =
          `Exercício ${data.etapa + 1} de ${data.total}`;
      }

      let porcentagem = (data.etapa / data.total) * 100;
      document.getElementById("progressFill").style.width = porcentagem + "%";
    });
}

function iniciarVoz() {
  let recognition = new webkitSpeechRecognition();
  recognition.lang = "pt-BR";

  recognition.start();

  recognition.onresult = function(event) {
    let texto = event.results[0][0].transcript;

    fetch("/verificar", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({resposta: texto})
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById("resultado").innerText =
        data.resultado === "correto" ? "✅ Correto!" : "❌ Tente novamente";

      atualizarTela(data.etapa, data.total);
    });
  };
}

function resetar() {
  fetch("/reset")
    .then(() => carregarProgresso());
}

carregarProgresso();
