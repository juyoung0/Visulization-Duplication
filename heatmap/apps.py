from django.apps import AppConfig
import heatmap

class HeatmapConfig(AppConfig):
    name = 'heatmap'

    def ready(self):
        """
        Perform initialization tasks.
        """
        from .models import geromicsData, member, block, session, session_history, closed_block, log_history, block_annotation_history, project, goa_human, go_obo
        heatmap.geromicsData = geromicsData
        heatmap.member = member
        heatmap.block = block
