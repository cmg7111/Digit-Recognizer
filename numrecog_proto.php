<!DOCTYPE html>
<html lang="en">
  <head>
     <meta charset="utf-8">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
     <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="favicon.ico">
	<!-- In header -->
	<link rel="stylesheet" href="jquery.lineProgressbar.css">

    <link type="text/css" rel="stylesheet" href="style.css">

    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">

    <title>NUMFIND</title>


 <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <style type="text/css">



    </style>
  </head>


  <body>

    <!--<div class="menubar">
      <ul>
        <li><a href="numrecog.php">Digit Recognizer</a></li>
      </ul>
    </div>-->
      

    <!-- Main jumbotron for a primary marketing message or call to action -->
    <div id="page-wrapper">
        <div id="sidebar-wrapper">
    <ul class="sidebar-nav">
      <li class="sidebar-brand">
        <font color="#999">Digit Rcognizer</font>
      </li>
      <li><a href="/numrecog/numrecog.php"><img src="car_icon.png"> &nbsp&nbsp자동차 번호판</img></a></li>
      <!--<li><a href="/numrecog/numrecog2.php"><img src="card_icon.png">  &nbsp&nbsp신용카드</img></a></li>-->
    </ul>
  </div>
  <div class="main-wrapper">
     <div class="jumbotron">
      <div class="container">
        <h1>Digit Recognizer - Car Number Plates</h1>
        <p>업로드한 자동차 이미지 내에서 번호판 숫자를 인식하여 출력합니다.
      </div>
    </div>

  
<script type="text/javascript">
</script>
<div class="container"  align="center">
      <!-- Example row of columns -->
      <div class="row">
       <article class="container">
			<div id="holder">
			</div> 
			<div id="result" class="scrollbar" id="style-2">
                <div class="force-overflow">
				<table id="resulttable">
					<tbody>
							<th>Image</th>
							<th>Result</th>
							<th>Confidence</th>
					</tbody>
					<tbody id="tb"></tbody>
				</table>
                </div>
			</div>
    	</article>

       </div>
	
      <hr>

      <footer align="left">
        <p>&copy; 굿모닝아이텍</p>
      </footer>
    </div> 	
</div>
      </div>
  <!-- /container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
   <!-- In footer -->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
	<script src="jquery.lineProgressbar.min.js"></script>

    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
  </body>
</html>

<script>

    var holder = document.getElementById('holder');
    var cnt=0;
         
    holder.ondragover = function () { this.className = 'hover'; return false; };
    holder.ondragend = function () { this.className = 'a'; return false; };
    holder.ondrop = function (e) {
        this.className = 'a';
        e.preventDefault();
        

        readfiles(e.dataTransfer.files);
    }
    cnt=cnt+1;
 	var res;
    var flag=false;
    var btnflag=false;

    function readfiles(files) {
        // 파일 미리보기
        var table=document.getElementById('tb');
        var formData = new FormData();
        formData.append('upload', files[0]);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', './upload.php');
        xhr.responseType = 'json'
        xhr.send(formData);

        if(document.getElementById("uploaded")){
            var imgEle = document.getElementById("uploaded");
            flag=true;
            holder.removeChild(imgEle);
            table.innerHTML="";
        }
        var image = new Image();
        image.src = './loading.gif'
        image.id="uploaded"
        holder.appendChild(image);


        // 이미지 작업 완료 시 
        xhr.onreadystatechange = function() {
          if (xhr.readyState  == xhr.DONE)     {
            if (xhr.status === 200) { 
            	//var list = JSON.parse(xhr.response);
                var imgEle = document.getElementById("uploaded");
            	res=xhr.response;
                var mybtn=document.createElement("BUTTON");
                mybtn.classList.add("btn","btn-success");
                mybtn.type="button";
                mybtn.value="false";
                mybtn.id="btn";
                mybtn.innerHTML="결과 출력";
                holder.appendChild(mybtn);
                holder.removeChild(imgEle);

                $('#btn').click(function(){
                    btnflag=true;
                    console.log(btnflag);
                    $('#btn').remove();
                    previewfile(files[0]);
                } )
                
            }
          }
        }

    }
    
    function previewfile(file) {
        var reader = new FileReader();
        reader.onload = function (event) {
        	var imgEle = document.getElementById("uploaded");
            var image = new Image();
            image.src = './output.jpg'+'?_='+ new Date().getTime();
            image.width=540;
            image.id="uploaded"
            if(imgEle){
                holder.removeChild(imgEle);
            } 
            
            if(flag==true){
                console.log("있어");
                image.src = './output.jpg'+'?_='+ new Date().getTime();
                holder.appendChild(image);
            }
            else{
                console.log("없어");
            	holder.appendChild(image);
            }
            image.onload=function(){
                Result();
            }
        };
        
        reader.readAsDataURL(file);
        
    }

    function Result(){
    	src='getfile.php';

    	var result = document.getElementById('result');
    	var table=document.getElementById('tb');
    	var filenames = <?php $out = array();
                    foreach (glob('numimg/*.jpg') as $filename) {
                        $p = pathinfo($filename);
                        $out[] = $p['filename'];
                    }
                    echo json_encode($out); ?>;


    	for(var i=0;i<=res[2][0];i++){
    		var row=table.insertRow(table.rows.length);
    		var cell1=row.insertCell(0);
    		var cell2=row.insertCell(1);
    		var cell3=row.insertCell(2);
            cell3.style.width="230px";
            var image = new Image();
            var node = document.createElement('p');
            node.innerHTML=res[0][i];

            var node2 = document.createElement('div');
            node2.id='progressbar'+i.toString();
            
            //node2.innerHTML=res[1][i];
            
            image.src = 'numimg/crop_'+i+'.jpg'+'?_='+ new Date().getTime();;
            image.id="result"
            image.width=50;
            image.height=40;
            cell1.appendChild(image);
            cell2.appendChild(node);
            cell3.appendChild(node2);
            addbar(node2.id,res[1][i]);
    	}
    }

    function addbar(id,confi){
    	confi=confi*100;
    	if(confi>90)
    		color='#81DAF5';
        else if(confi>80)
            color='#1abc9c';
    	else if(confi>60)
    		color='#e67e22';
    	else if(confi>40)
    		color='#f1c40f';
    	else
    		color='#FA5858';

    	$('#'+id).LineProgressbar({
				percentage: confi, fillBackgroundColor: color
			});
    }

</script>
