<html>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.1/chart.js" integrity="sha512-Lii3WMtgA0C0qmmkdCpsG0Gjr6M0ajRyQRQSbTF6BsrVh/nhZdHpVZ76iMIPvQwz1eoXC3DmAg9K51qT5/dEVg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<body>

Welcome, Weaver ID <?php echo $_POST["Weav_ID"]; ?><br>

<centre><canvas id="myChart" width="50" height="10" ></canvas></centre> 
  <script>
       const plugin = {
  id: 'custom_canvas_background_color',
  beforeDraw: (chart) => {
    const ctx = chart.canvas.getContext('2d');
    ctx.save();
    ctx.globalCompositeOperation = 'destination-over';
    ctx.fillStyle = 'lightYellow';
    ctx.fillRect(0, 0, chart.width, chart.height);
    ctx.restore();
  }
};
          let Labels = ['January','February','March','April','May','June','July','August','September','October','November','December'];
          let Quantity =[0,0,0,0,0,0,0,0,0,0,0,0];
      productData();
      async function productData(){
          const url= 'http://127.0.0.1:5500/Reshamandi/random_data_2.csv';
          const response = await fetch(url);
          const tabledata = await response.text();
          const table = tabledata.split('\n').slice(1);
          console.log("PHP "+typeof(<?php echo $_POST["Weav_ID"]; ?>));
           var i=1;
          table.forEach(row =>{
            const column=row.split(',');
            const Weaver_ID=column[0];
            
            if(i==1){
            console.log("ID "+typeof(parseInt(Weaver_ID)));
            i+=1;
            }
            if((<?php echo $_POST["Weav_ID"]; ?>)==parseInt(Weaver_ID)){
            switch(column[7]) {
                case 'January' : Quantity[0]+=column[2]; break;
                case 'February': Quantity[1]+=column[2]; break;
                case 'March': Quantity[2]+=column[2]; break;
                case 'April': Quantity[3]+=column[2]; break;
                case 'May':Quantity[4]+=column[2]; break; 
                case 'June':Quantity[5]+=column[2]; break;
                case 'July':Quantity[6]+=column[2]; break;
                case 'August':Quantity[7]+=column[2]; break;
                case 'September':Quantity[8]+=column[2]; break; 
                case 'October':Quantity[9]+=column[2]; break;
                case 'November':Quantity[10]+=column[2]; break;
                case 'December':Quantity[11]+=column[2]; break;
                            
            }
      }});
        
           
  console.log(Labels);
  console.log(Quantity);
  const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: Labels,
        datasets: [{
            
            data: Quantity,
            backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)',
                'rgba(255, 159, 64, 0.5)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            hoverOffset: 5,
            borderWidth: 1,
            tension: 0.4,
        }
        ]
    },
    plugins: [plugin],
    options: {
        plugins: {
            title: {
                display: true,
                text: 'Quantity vs Month'
            },

        },
        scales: {
            y: {
                beginAtZero: false
            }
        }
    
    }
});

      }

  </script>
</body>
</html>