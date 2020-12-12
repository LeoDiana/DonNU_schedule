$(function(){

    var $cat = $("#category1"),
        $subcat = $(".subcat");


    $subcat.each(function(i,v){
    	var $e = $(v);
    	var _id = $e.attr("id");
    });


    var _lastRel;
    $cat.on("change",function(){
        var _rel = $(this).val();
        if(_lastRel === _rel) return true;
        _lastRel = _rel;
        $subcat.find("option").attr("style","");
        $subcat.val("");
        $subcat.find(".is-dyn").remove();
        if(!_rel) return $subcat.prop("disabled",true);
        $subcat.each(function(){
        	var $el = $(this);
          var _id = $el.attr("id");
        });
        $subcat.prop("disabled",false);
    });

});