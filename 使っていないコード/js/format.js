$("#createVideoPage").on("click", function() {
  var template = '<iframe src="http://127.0.0.1:5000/watchVideo" style="width:100%; height: 700px"></iframe>'
  $("#main").append(template);
});

function sendAjax(senddata, url){
	// senddataは辞書型
      $.ajax({
        data : senddata,
        type : 'post',
        url : url
      })
      .done(function(data){
      	console.log("recieved!");
      });
}

//任意のタブにURLからリンクするための設定
function GethashID (hashIDName){
  if(hashIDName){
    //タブ設定
    $('.tab li').find('a').each(function() { //タブ内のaタグ全てを取得
      var idName = $(this).attr('href'); //タブ内のaタグのリンク名（例）#lunchの値を取得 
      if(idName == hashIDName){ //リンク元の指定されたURLのハッシュタグ（例）http://example.com/#lunch←この#の値とタブ内のリンク名（例）#lunchが同じかをチェック
        var parentElm = $(this).parent(); //タブ内のaタグの親要素（li）を取得
        $('.tab li').removeClass("active"); //タブ内のliについているactiveクラスを取り除き
        $(parentElm).addClass("active"); //リンク元の指定されたURLのハッシュタグとタブ内のリンク名が同じであれば、liにactiveクラスを追加
        //表示させるエリア設定
        $(".area").removeClass("is-active"); //もともとついているis-activeクラスを取り除き
        $(hashIDName).addClass("is-active"); //表示させたいエリアのタブリンク名をクリックしたら、表示エリアにis-activeクラスを追加 
      }
    });
  }
}

//タブをクリックしたら
$('.tab a').on('click', function() {
  var idName = $(this).attr('href'); //タブ内のリンク名を取得  
  GethashID (idName);//設定したタブの読み込みと
  return false;//aタグを無効にする
});


// 上記の動きをページが読み込まれたらすぐに動かす
$(window).on('load', function () {
    $('.tab li:first-of-type').addClass("active"); //最初のliにactiveクラスを追加
    $('.area:first-of-type').addClass("is-active"); //最初の.areaにis-activeクラスを追加
  var hashName = location.hash; //リンク元の指定されたURLのハッシュタグを取得
  GethashID (hashName);//設定したタブの読み込み
});

// $(document).ready(function() {
//     // ナビゲーションリンクのクリックイベントを追加
//     $(".nav-link").click(function(event) {
//         event.preventDefault(); // リンクのデフォルト動作を無効化
//         var url = $(this).attr("href"); // リンク先URLを取得

//         // Ajaxリクエストを送信
//         $.ajax({
//             url: "watchVideoContent",
//             type: "GET",
//             dataType: "html", // 取得するデータの形式を指定
//             success: function(data) {
//                 // Ajaxリクエストが成功した場合、ページコンテンツを更新
//                 $("#main").html(data);
//             },
//             error: function(xhr, status, error) {
//                 // エラーハンドリング
//                 console.error(xhr.responseText);
//             }
//         });
//     });
// });

$(document).ready(function() {
    $('a.useAjax').click(function(event) {
        event.preventDefault();  // デフォルトのリンク動作を停止
        var url = $(this).attr('href');  // リンクのURLを取得

        $.ajax({
            url: url,
            method: 'GET',
            success: function(response) {
                // $('#content').html(response);  // 取得したコンテンツを挿入
            },
            error: function() {
                // $('#content').html('<p>Error loading content.</p>');  // エラーメッセージを表示
            }
        });
    });
});
