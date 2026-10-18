import sys

class InfiniteMemoryBuffer:
    def __init__(self):
        self.storage = []
        self.total_bytes_ingested = 0

    def swallow_stream(self, data_packet):
        """Appends raw environmental data arrays directly into unconstrained memory."""
        self.storage.append(data_packet)
        self.total_bytes_ingested += sys.getsizeof(data_packet)

    def clear_buffer(self):
        self.storage.clear()
        self.total_bytes_ingested = 0

    def get_allocation_metrics(self):
        return {
            "allocated_blocks": len(self.storage),
            "total_memory_mass_bytes": self.total_bytes_ingested
  }
      
