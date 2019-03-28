// 搜索数据表格初始化
layui.use( 'table', function(){
  var table = layui.table;
  
  table.render({
    elem: '#test'
    ,url: "/normal/search"
    ,cellMinWidth: 80 //全局定义常规单元格的最小宽度，layui 2.2.1 新增
    ,page: { //支持传入 laypage 组件的所有参数（某些参数除外，如：jump/elem） - 详见文档
                  layout: ['limit', 'count', 'prev', 'page', 'next', 'skip'] //自定义分页布局
                  ,curr: 1 //设定初始在第 1 页
                  ,groups: 5//只显示 1 个连续页码
                  // ,first: false //不显示首页
                  // ,last: false //不显示尾页
                }
    ,cols: [[
      {field:'title', width:'25%', title: '标题'}
      ,{field:'content', title: '内容', width: '23%'}
      ,{field:'sentiment', width:'7%', title: '情感'}
      ,{field:'type', width:'7%', title: '类型'}
      ,{field:'keywords', title: '关键词', width: '21%'} //minWidth：局部定义当前单元格的最小宽度，layui 2.2.1 新增
      ,{field:'source', title: '来源', width:'10%'}
      ,{field:'newsDate', title: '日期',width:'7.3%'}
    ]]
  });
});

// 搜索数据表格获取数据
function search_layui(){
    var url = "/normal/search";
    var params = {"question":document.getElementById("question").value};
    layui.use( 'table', function(){
        var tableIns = layui.table;

        tableIns.render({
          elem: '#test'
          ,url: url //设置异步接口
          ,where: params
          ,page: { //支持传入 laypage 组件的所有参数（某些参数除外，如：jump/elem） - 详见文档
                  layout: ['limit', 'count', 'prev', 'page', 'next', 'skip'] //自定义分页布局
                  ,curr: 1 //设定初始在第 1 页
                  ,groups: 5//只显示 1 个连续页码
                  // ,first: false //不显示首页
                  // ,last: false //不显示尾页
                }
          ,done: function (res, curr, count) {// 表格渲染完成之后的回调
                // $(".layui-table th").css("font-weight", "bold");// 设定表格标题字体加粗
                LayUIDataTable.SetJqueryObj($);// 第一步：设置jQuery对象
                var currentRowDataList = LayUIDataTable.ParseDataTable(function (index, currentData, rowData) {
                })
                // LayUIDataTable.HideField('sentiment');// 隐藏列-单列模式
                // 对相关数据进行判断处理--此处对mk2大于30的进行高亮显示
                $.each(currentRowDataList, function (index, obj) {
                    if (obj['sentiment'] && obj['sentiment'].value == '负面') {
                        obj['sentiment'].row.css({"background-color": " #FF7F50", "color": "black"});
                    }
                })
            }
          ,cols: [[
              {field:'title', width:'25%', title: '标题'}
              ,{field:'content', title: '内容', width: '23%'}
              ,{field:'sentiment', width:'7%', title: '情感'}
              ,{field:'type', width:'7%', title: '类型'}
              ,{field:'keywords', title: '关键词', width: '21%'} //minWidth：局部定义当前单元格的最小宽度，layui 2.2.1 新增
              ,{field:'source', title: '来源', width:'10%'}
              ,{field:'newsDate', title: '日期',width:'7.3%'}
            ]]
        }); 

    });
}

// 获取情感模型预测结果
function sentiment_predict(){
    var url = "http://localhost:8585/nlp/sentiment";
    var body = JSON.stringify({"news":[document.getElementById("sentiment_text").value]});
    console.log(body)

    $.ajax({
      type: 'post',
      url: url,
      data: body,
      dataType: 'json',
      "success": function(data){
        alert("情感："+data.data[0]);
      },
      "error": function(result){
        alert(result);
      }
    });
}

// 获取类型模型预测结果
function type_predict(){
    var url = "http://localhost:8585/nlp/news_type";
    var body = JSON.stringify({"news":[document.getElementById("type_text").value]});
    console.log(body);

    $.ajax({
      type: 'post',
      url: url,
      data: body,
      dataType: 'json',
      "success": function(data){
        alert("新闻类型："+data.data[0]);
      },
      "error": function(result){
        alert(result);
      }
    });
}

// 搜索输入框回车事件
function keyup_submit(e){ 
 var evt = window.event || e; 
  if (evt.keyCode == 13){
    search_layui();
  }
}

