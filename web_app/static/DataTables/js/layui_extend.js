var LayUIDataTable = (function () {
    var rowData = {};
    var $;

    function checkJquery () {
        if (!$) {
            console.log("未获取jquery对象，请检查是否在调用ConvertDataTable方法之前调用SetJqueryObj进行设置！")
            return false;
        } else return true;
    }

    /**
     * 转换数据表格。
     * @param callback 双击行的回调函数，该回调函数返回三个参数，分别为：当前点击行的索引值、当前点击单元格的值、当前行数据
     * @returns {Array} 返回当前数据表当前页的所有行数据。数据结构：<br/>
     * [
     *      {字段名称1:{value:"当前字段值",cell:"当前字段所在单元格td对象",row:"当前字段所在行tr对象"}}
     *     ,{字段名称2:{value:"",cell:"",row:""}}
     * ]
     * @constructor
     */
    function ConvertDataTable (callback) {
        if (!checkJquery()) return;
        var dataList = [];
        var rowData = {};
        var trArr = $(".layui-table-body.layui-table-main tr");// 行数据
        if (!trArr || trArr.length == 0) {
            console.log("未获取到相关行数据，请检查数据表格是否渲染完毕！");
            return;
        }
        $.each(trArr, function (index, trObj) {
            var currentClickRowIndex;
            var currentClickCellValue;

            $(trObj).dblclick(function (e) {
                var returnData = {};
                var currentClickRow = $(e.currentTarget);
                currentClickRowIndex = currentClickRow.data("index");
                currentClickCellValue = e.target.innerHTML
                $.each(dataList[currentClickRowIndex], function (key, obj) {
                    returnData[key] = obj.value;
                });
                callback(currentClickRowIndex, currentClickCellValue, returnData);
            });
            var tdArrObj = $(trObj).find('td');
            rowData = {};
            //  每行的单元格数据
            $.each(tdArrObj, function (index_1, tdObj) {
                var td_field = $(tdObj).data("field");
                rowData[td_field] = {};
                rowData[td_field]["value"] = $($(tdObj).html()).html();
                rowData[td_field]["cell"] = $(tdObj);
                rowData[td_field]["row"] = $(trObj);

            })
            dataList.push(rowData);
        })
        return dataList;
    }

    return {
        /**
         * 设置JQuery对象，第一步操作。如果你没有在head标签里面引入jquery且未执行该方法的话，ParseDataTable方法、HideField方法会无法执行，出现找不到 $ 的错误。如果你是使用LayUI内置的Jquery，可以
         * var $ = layui.jquery   然后把 $ 传入该方法
         * @param jqueryObj
         * @constructor
         */
        SetJqueryObj: function (jqueryObj) {
            $ = jqueryObj;
        }

        /**
         * 转换数据表格
         */
        , ParseDataTable: ConvertDataTable

        /**
         * 隐藏字段
         * @param fieldName 要隐藏的字段名（field名称）参数可为字符串（隐藏单列）或者数组（隐藏多列）
         * @constructor
         */
        , HideField: function (fieldName) {
            if (!checkJquery()) return;
            if (fieldName instanceof Array) {
                $.each(fieldName, function (index, field) {
                    $("[data-field='" + field + "']").css('display', 'none');
                })
            } else if (typeof fieldName === 'string') {
                $("[data-field='" + fieldName + "']").css('display', 'none');
            } else {

            }
        }
    }
})();