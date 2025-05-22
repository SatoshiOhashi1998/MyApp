// popup.js

document.addEventListener('DOMContentLoaded', function() {
    // イベントリスナーの追加
    document.getElementById('calculateButton').addEventListener('click', calculateExpectedValue);
});

function calculateExpectedValue() {
    // 入力値を取得
    const oddsA = parseFloat(document.getElementById('oddsA').value);
    const oddsB = parseFloat(document.getElementById('oddsB').value);

    if (isNaN(oddsA) || isNaN(oddsB) || oddsA <= 1 || oddsB <= 1) {
        alert('倍率は1より大きい必要があります');
        return;
    }

    // 期待値が高くなる確率を計算
    let betterOdds, otherOdds, betterEvent, threshold;

    if (oddsA < oddsB) {
        betterOdds = oddsA;
        otherOdds = oddsB;
        betterEvent = "チームA";
    } else {
        betterOdds = oddsB;
        otherOdds = oddsA;
        betterEvent = "チームB";
    }

    // 確率の閾値を計算
    threshold = (otherOdds - 1) / (betterOdds + otherOdds - 2);

    // 結果を表示
    document.getElementById('result').textContent = 
        `${betterEvent}（倍率が小さい方、${betterOdds}）に賭けると期待値が高くなるための確率の閾値は ${ (threshold * 100).toFixed(1) }% です。`;
}
