/**
 * Created by dryji on 2017-02-20.
 * managing unit annotations integrated with its modal
 */
(function (parent) {
    _.extend(parent, {
        createUnitAnnotation: function ($block) {
            var obj = {
                username: userManager.USERNAME,
                project_name: userManager.PROJECT,
                session_name: userManager.SESSION,
                session_ver: userManager.SESSION_VER,
                block_iden: $block.data().req.block_iden,
                block_ver: $block.data().req.block_ver,
                author: $('input.input-author-note').val(),
                date: $('input.input-data-note').val(),
                data_annotation: $('textarea.input-data-note').val(),
                research_annotation: $('textarea.input-research-note').val(),
                experiment_type: $('input.input-experiment-note').val(),
                platform_name: $('input.input-platform-note').val(),
                organism: $('input.input-organism-note').val()
            };
            return $.ajax({
                url: "createBlockAnnotation.html", method: 'post', data: {
                    username: userManager.USERNAME,
                    project_name: userManager.PROJECT,
                    session_name: userManager.SESSION,
                    session_ver: userManager.SESSION_VER,
                    block_iden: $block.data().req.block_iden,
                    block_ver: $block.data().req.block_ver,
                    block_annotation: JSON.stringify(obj)
                }, error: userManager.failAjax,
                success: function (data, status) {
                    unitManager.btnAddUnitAnnotation(data, status);
                    unitManager.logger('Create-Unit-Annotation', {
                        username: userManager.USERNAME,
                        project_name: userManager.PROJECT,
                        session_name: userManager.SESSION,
                        session_ver: userManager.SESSION_VER,
                        block_name: $block.data().req.block_name,
                        block_iden: $block.data().req.block_iden,
                        block_ver: $block.data().req.block_ver,
                        block_annotation: JSON.stringify(obj)
                    });
                }
            });

        },
        btnAddUnitAnnotation: function (data, status) {
            if (!data.success) return userManager.failAjax(data, status);
            console.log(data);
            $('#annotation-modal').modal('hide');
            unitManager.getAnnotations(unitManager.SELECTED.data().res.annotation_path);
        },
        getAnnotations: function (path, $block) {
            return $.ajax({
                url: path,
                method: 'POST',
                error: userManager.failAjax,
                success: function (data, status) {
                    unitManager.addUnitAnnotation(data, status, $block)
                }
            })
        },
        addUnitAnnotation: function (data, status, $block) {
            //if (!data.success) return userManager.failAjax(data,status);
            if ($block == null) $block = unitManager.SELECTED;
            $block.find('.annotation-item').remove();
            var $anno = $block.find('.annotation');
            _.forEach(data.annotation_list, function (item, idx) {
                var $note = $('<li class="annotation-item"><a data-trigger="hover click" data-toggle="popover" data-placement="right"><span class="badge">' + idx + '</span></a></li>');
                $anno.append($note);
                $note.find('a').attr('title', "<a class='btn btn-xs btn-danger delete-unit-annotation btn-block' id='anno-" + idx + "' onClick='unitManager.deleteUnitAnnotation(this)'>DELETE</div>");
                var content = "<div style='z-index: 50'>" +
                    "<div class='badge'>Auhtor</div><pre>" + item.annotation.author + "</pre>" +
                    "<div class='badge'>Date</div><pre>" + item.annotation.date + "</pre>" +
                    "<div class='badge'>Data</div><pre>" + item.annotation.data_annotation + "</pre>" +
                    "<div class='badge'>Cluster</div><pre>" + item.annotation.data_annotation + "</pre>" +
                    "<div class='badge'>Experiment Type</div><pre>" + item.annotation.experiment_type + "</pre>" +
                    "<div class='badge'>Organism</div><pre>" + item.annotation.organism + "</pre>" +
                    "<div class='badge'>Research</div><pre>" + item.annotation.research_annotation + "</pre>" +
                    "<div class='badge'>Platform</div><pre>" + item.annotation.platform_name + "</pre>"+
                "</div>";


                $note.find('a').attr('data-content', content);
                $note.find('.delete-unit-annotation').on('click', function (e) {
                    console.log('delete', this, $(this).parent);
                });
                $note.find('a').on('click', function () {
                    $('[data-toggle="popover"]').popover('hide');
                    $(this).popover('toggle');
                });
            });
            $('[data-toggle="popover"]').popover({html: true});
        },
        deleteUnitAnnotation: function (item) {
            var idx = $(item).attr('id').split('-')[1];
            console.log(idx);
            $.post("deleteBlockAnnotation.html", {
                username: userManager.USERNAME,
                session_name: userManager.SESSION,
                session_ver: userManager.SESSION_VER,
                block_iden: unitManager.SELECTED.data().req.block_iden,
                project_name: unitManager.SELECTED.data().req.project_name,
                block_ver: unitManager.SELECTED.data().req.block_ver,
                annotation_num: idx
            }, function (data, status) {
                unitManager.getAnnotations(unitManager.SELECTED.data().res.annotation_path);
                unitManager.logger('Delete-Unit-Annotation', {
                    username: userManager.USERNAME,
                    session_name: userManager.SESSION,
                    session_ver: userManager.SESSION_VER,
                    block_name: unitManager.SELECTED.data().req.block_name,
                    block_iden: unitManager.SELECTED.data().req.block_iden,
                    project_name: unitManager.SELECTED.data().req.project_name,
                    block_ver: unitManager.SELECTED.data().req.block_ver,
                    annotation_num: idx
                });
            });

        }
    })
})(unitManager);