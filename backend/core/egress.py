from dataclasses import dataclass
from ipaddress import ip_address

@dataclass(frozen=True)
class EgressPolicy:
    allowed_hosts: frozenset[str]
    allowed_ports: frozenset[int] = frozenset({443})
    def __post_init__(self):
        hosts=frozenset(h.rstrip('.').lower() for h in self.allowed_hosts)
        object.__setattr__(self,"allowed_hosts",hosts)
        if not hosts: raise ValueError("egress allowlist must not be empty")
        if any(p<1 or p>65535 for p in self.allowed_ports): raise ValueError("invalid port")
    def authorize(self, host: str, port: int) -> None:
        normalized=host.rstrip('.').lower()
        if port not in self.allowed_ports: raise PermissionError("egress port is not allowed")
        if normalized in self.allowed_hosts: return
        try: address=ip_address(normalized)
        except ValueError: address=None
        if address is not None: raise PermissionError("literal IP egress is not allowed")
        raise PermissionError("egress host is not on the allowlist")
