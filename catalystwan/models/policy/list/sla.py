from typing import List, Literal, Optional
from uuid import UUID

from catalystwan.models.policy.lists_entries import SLAClassListEntry
from catalystwan.models.policy.policy_list import PolicyListBase, PolicyListId, PolicyListInfo


class SLAClassList(PolicyListBase):
    type: Literal["sla"] = "sla"
    entries: List[SLAClassListEntry] = []

    def assign_app_probe_class(
        self,
        app_probe_class_id: UUID,
        latency: Optional[int] = None,
        loss: Optional[int] = None,
        jitter: Optional[int] = None,
    ) -> SLAClassListEntry:
        # SLA class list must have only one entry!
        _latency = str(latency) if latency is not None else None
        _loss = str(loss) if loss is not None else None
        _jitter = str(jitter) if jitter is not None else None
        entry = SLAClassListEntry(latency=_latency, loss=_loss, jitter=_jitter, app_probe_class=app_probe_class_id)
        self._add_entry(entry, single=True)
        return entry

    def add_fallback_jitter_criteria(self, jitter_variance: int) -> None:
        assert self.entries, "Assign app probe class before configuring best fallback tunnel"
        self.entries[0].add_fallback_jitter_criteria(jitter_variance)

    def add_fallback_latency_criteria(self, latency_variance: int) -> None:
        assert self.entries, "Assign app probe class before configuring best fallback tunnel"
        self.entries[0].add_fallback_latency_criteria(latency_variance)

    def add_fallback_loss_criteria(self, loss_variance: int) -> None:
        assert self.entries, "Assign app probe class before configuring best fallback tunnel"
        self.entries[0].add_fallback_loss_criteria(loss_variance)


class SLAClassListEditPayload(SLAClassList, PolicyListId):
    pass


class SLAClassListInfo(SLAClassList, PolicyListInfo):
    pass
