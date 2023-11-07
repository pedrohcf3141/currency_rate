// Função para buscar os dados do endpoint
function fetchData(startDate, endDate) {
    fetch(`http://localhost:8000/currency_quotes?start_date=${startDate}&end_date=${endDate}`)
        .then(response => response.json())
        .then(data => {
            // Renderiza o gráfico com os dados recebidos
            renderChart(data);
        });
 }
 
 // Função para renderizar o gráfico
 function renderChart(data) {
    Highcharts.chart('container', {
        title: {
            text: 'Cotações de Moedas'
        },
        xAxis: {
            type: 'datetime'
        },
        yAxis: {
            title: {
                text: 'Taxa de Câmbio'
            }
        },
        series: [{
            name: 'Taxa de Câmbio',
            data: data.map(item => [new Date(item.date).getTime(), item.exchange_rate])
        }]
    });
 }
 
 // Chama a função fetchData com as datas de início e fim
 fetchData('2023-01-01', '2023-12-31');
 