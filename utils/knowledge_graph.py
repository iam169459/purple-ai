"""
Knowledge Graph
Structured knowledge representation with relationships and causal reasoning
"""
import json
import os
import time
from typing import Dict, Any, List, Optional, Set, Tuple
from logger import logger


# Edge/relationship types for the knowledge graph
RELATIONSHIP_TYPES = {
    "CAUSES": "A causes B",
    "PREVENTS": "A prevents B",
    "REQUIRES": "A requires B",
    "LEADS_TO": "A leads to B",
    "INFLUENCES": "A influences B",
    "SIMILAR_TO": "A is similar to B",
    "PART_OF": "A is part of B",
    "CONTRASTS_WITH": "A contrasts with B",
    "RELATED": "A is related to B (generic)"
}


class KnowledgeEdge:
    """A typed edge between two concepts"""
    def __init__(self, source: str, target: str, relationship: str, 
                 confidence: float = 0.5, data: Dict[str, Any] = None):
        self.source = source
        self.target = target
        self.relationship = relationship
        self.confidence = confidence
        self.data = data or {}
        self.created_at = time.time()
        self.strength = 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "relationship": self.relationship,
            "confidence": self.confidence,
            "data": self.data,
            "created_at": self.created_at,
            "strength": self.strength
        }
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'KnowledgeEdge':
        edge = cls(d["source"], d["target"], d["relationship"], 
                   d.get("confidence", 0.5), d.get("data", {}))
        edge.created_at = d.get("created_at", time.time())
        edge.strength = d.get("strength", 1.0)
        return edge

class KnowledgeNode:
    """A node in the knowledge graph"""
    def __init__(self, concept: str, category: str = "general", 
                 data: Dict[str, Any] = None, source: str = ""):
        self.concept = concept
        self.category = category
        self.data = data or {}
        self.source = source
        self.created_at = time.time()
        self.updated_at = time.time()
        self.confidence = 0.5
        self.access_count = 0
        self.related = set()  # Set of related concept names
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "concept": self.concept,
            "category": self.category,
            "data": self.data,
            "source": self.source,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "confidence": self.confidence,
            "access_count": self.access_count,
            "related": list(self.related)
        }
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'KnowledgeNode':
        node = cls(d["concept"], d.get("category", "general"), d.get("data", {}), d.get("source", ""))
        node.created_at = d.get("created_at", time.time())
        node.updated_at = d.get("updated_at", time.time())
        node.confidence = d.get("confidence", 0.5)
        node.access_count = d.get("access_count", 0)
        node.related = set(d.get("related", []))
        return node

class KnowledgeGraph:
    """
    Graph-based knowledge system.
    Nodes = concepts/topics, Edges = relationships between concepts.
    """
    
    def __init__(self, storage_path: str = "data/knowledge_graph.json"):
        self.storage_path = storage_path
        self.nodes = {}  # concept -> KnowledgeNode
        self.categories = {}  # category -> set of concepts
        self.edges = []  # List of KnowledgeEdge
        self.edge_index = {}  # concept -> list of edges involving it
        self._load()
        logger.info(f"🧠 Knowledge Graph initialized | {len(self.nodes)} concepts, {len(self.edges)} edges loaded")
    
    def _load(self):
        """Load knowledge graph from disk"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for concept, node_data in data.get("nodes", {}).items():
                        self.nodes[concept] = KnowledgeNode.from_dict(node_data)
                    self.categories = {k: set(v) for k, v in data.get("categories", {}).items()}
                    # Load edges
                    for edge_data in data.get("edges", []):
                        edge = KnowledgeEdge.from_dict(edge_data)
                        self.edges.append(edge)
                        # Build edge index
                        for concept in [edge.source, edge.target]:
                            if concept not in self.edge_index:
                                self.edge_index[concept] = []
                            self.edge_index[concept].append(edge)
                logger.info(f"📚 Loaded {len(self.nodes)} knowledge nodes, {len(self.edges)} edges")
        except Exception as e:
            logger.error(f"Error loading knowledge graph: {e}")
            self.nodes = {}
            self.categories = {}
            self.edges = []
            self.edge_index = {}
    
    def save(self):
        """Save knowledge graph to disk"""
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            data = {
                "nodes": {c: n.to_dict() for c, n in self.nodes.items()},
                "categories": {k: list(v) for k, v in self.categories.items()},
                "edges": [e.to_dict() for e in self.edges],
                "saved_at": time.time()
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"💾 Knowledge graph saved: {len(self.nodes)} nodes, {len(self.edges)} edges")
            return True
        except Exception as e:
            logger.error(f"Error saving knowledge graph: {e}")
            return False
    
    def add_knowledge(self, concept: str, data: Dict[str, Any], 
                      category: str = "general", source: str = "",
                      related_concepts: List[str] = None,
                      confidence: float = 0.5) -> KnowledgeNode:
        """Add or update knowledge about a concept"""
        concept_lower = concept.lower().strip()
        
        if concept_lower in self.nodes:
            # Update existing
            node = self.nodes[concept_lower]
            node.data.update(data)
            node.updated_at = time.time()
            node.confidence = max(node.confidence, confidence)
            if source:
                node.source = source
            logger.info(f"🔄 Updated knowledge: '{concept}'")
        else:
            # Create new
            node = KnowledgeNode(concept, category, data, source)
            node.confidence = confidence
            self.nodes[concept_lower] = node
            logger.info(f"➕ New knowledge added: '{concept}' [{category}]")
        
        # Update category index
        if category not in self.categories:
            self.categories[category] = set()
        self.categories[category].add(concept_lower)
        
        # Add relationships
        if related_concepts:
            for related in related_concepts:
                rel_lower = related.lower().strip()
                node.related.add(rel_lower)
                # Bidirectional relationship
                if rel_lower in self.nodes:
                    self.nodes[rel_lower].related.add(concept_lower)
        
        return node
    
    def query(self, concept: str) -> Optional[KnowledgeNode]:
        """Query knowledge about a concept"""
        concept_lower = concept.lower().strip()
        node = self.nodes.get(concept_lower)
        if node:
            node.access_count += 1
            node.updated_at = time.time()
        return node
    
    def search(self, query: str, limit: int = 5) -> List[KnowledgeNode]:
        """Search for concepts matching query"""
        query_lower = query.lower()
        matches = []
        
        for concept, node in self.nodes.items():
            score = 0
            # Exact match
            if query_lower == concept:
                score += 100
            # Contains query
            elif query_lower in concept:
                score += 50
            # Query contains concept
            elif concept in query_lower:
                score += 30
            # Check in data
            data_str = str(node.data).lower()
            if query_lower in data_str:
                score += 20
            
            if score > 0:
                matches.append((score, node))
        
        # Sort by score descending, then by access count
        matches.sort(key=lambda x: (x[0], x[1].access_count), reverse=True)
        return [m[1] for m in matches[:limit]]
    
    def get_related(self, concept: str, depth: int = 1) -> List[str]:
        """Get related concepts up to a certain depth"""
        concept_lower = concept.lower().strip()
        if concept_lower not in self.nodes:
            return []
        
        related = set()
        current_level = {concept_lower}
        
        for _ in range(depth):
            next_level = set()
            for c in current_level:
                if c in self.nodes:
                    for r in self.nodes[c].related:
                        if r not in related and r != concept_lower:
                            related.add(r)
                            next_level.add(r)
            current_level = next_level
        
        return list(related)
    
    def get_by_category(self, category: str) -> List[KnowledgeNode]:
        """Get all knowledge in a category"""
        concepts = self.categories.get(category, set())
        return [self.nodes[c] for c in concepts if c in self.nodes]
    
    def forget(self, concept: str) -> bool:
        """Remove a concept from the graph"""
        concept_lower = concept.lower().strip()
        if concept_lower in self.nodes:
            node = self.nodes.pop(concept_lower)
            # Remove from categories
            for cat, concepts in self.categories.items():
                concepts.discard(concept_lower)
            # Remove from other nodes' relationships
            for n in self.nodes.values():
                n.related.discard(concept_lower)
            logger.info(f"🗑️  Forgot concept: '{concept}'")
            return True
        return False
    
    def export_report(self) -> str:
        """Generate a text report of the knowledge graph"""
        stats = self.get_stats()
        lines = [
            "=" * 50,
            "KNOWLEDGE GRAPH REPORT",
            "=" * 50,
            f"Total Concepts: {stats['total_concepts']}",
            f"Total Categories: {stats['total_categories']}",
            f"Total Relationships: {stats['total_relationships']}",
            f"Total Edges: {stats['total_edges']}",
            "",
            "Categories:",
        ]
        for cat, count in stats['categories_breakdown'].items():
            lines.append(f"  • {cat}: {count} concepts")
        
        lines.append("")
        lines.append("Edge Types:")
        for etype, count in stats.get("edge_types", {}).items():
            lines.append(f"  • {etype}: {count}")
        
        lines.append("")
        lines.append("Most Accessed Concepts:")
        for item in stats['most_accessed']:
            lines.append(f"  • {item['concept']}: {item['access_count']} accesses")
        
        lines.append("=" * 50)
        return "\n".join(lines)
    
    # ==================== CAUSAL REASONING ====================
    
    def add_edge(self, source: str, target: str, relationship: str, 
                 confidence: float = 0.5, data: Dict[str, Any] = None) -> KnowledgeEdge:
        """Add a typed edge between two concepts"""
        source_lower = source.lower().strip()
        target_lower = target.lower().strip()
        
        # Ensure both concepts exist as nodes
        for concept in [source_lower, target_lower]:
            if concept not in self.nodes:
                self.add_knowledge(concept, {"auto_created": True}, "auto")
        
        # Create edge
        edge = KnowledgeEdge(source_lower, target_lower, relationship.upper(), confidence, data)
        self.edges.append(edge)
        
        # Update edge index
        for concept in [source_lower, target_lower]:
            if concept not in self.edge_index:
                self.edge_index[concept] = []
            self.edge_index[concept].append(edge)
        
        # Also add to node's related set
        self.nodes[source_lower].related.add(target_lower)
        self.nodes[target_lower].related.add(source_lower)
        
        logger.info(f"🔗 Added edge: {source_lower} --[{relationship}]--> {target_lower}")
        self.save()
        return edge
    
    def add_causal_link(self, cause: str, effect: str, confidence: float = 0.5):
        """Add a causal relationship: cause CAUSES effect"""
        return self.add_edge(cause, effect, "CAUSES", confidence)
    
    def add_prevention(self, preventer: str, effect: str, confidence: float = 0.5):
        """Add a prevention relationship: preventer PREVENTS effect"""
        return self.add_edge(preventer, effect, "PREVENTS", confidence)
    
    def add_requirement(self, prerequisite: str, required: str, confidence: float = 0.5):
        """Add a requirement relationship: prerequisite REQUIRES required"""
        return self.add_edge(prerequisite, required, "REQUIRES", confidence)
    
    def add_similarity(self, concept_a: str, concept_b: str, confidence: float = 0.5):
        """Add a similarity relationship (bidirectional)"""
        edge = self.add_edge(concept_a, concept_b, "SIMILAR_TO", confidence)
        self.add_edge(concept_b, concept_a, "SIMILAR_TO", confidence)
        return edge
    
    def add_contrast(self, concept_a: str, concept_b: str, confidence: float = 0.5):
        """Add a contrast relationship (bidirectional)"""
        edge = self.add_edge(concept_a, concept_b, "CONTRASTS_WITH", confidence)
        self.add_edge(concept_b, concept_a, "CONTRASTS_WITH", confidence)
        return edge
    
    def add_influence(self, source: str, target: str, confidence: float = 0.5):
        """Add an influence relationship"""
        return self.add_edge(source, target, "INFLUENCES", confidence)
    
    def add_part_of(self, part: str, whole: str, confidence: float = 0.5):
        """Add a part-of relationship"""
        return self.add_edge(part, whole, "PART_OF", confidence)
    
    # ==================== CAUSAL QUERIES ====================
    
    def query_causes(self, effect: str) -> List[Dict[str, Any]]:
        """What causes this effect?"""
        effect_lower = effect.lower().strip()
        causes = []
        
        for edge in self.edges:
            if edge.target == effect_lower and edge.relationship in ["CAUSES", "LEADS_TO"]:
                causes.append({
                    "cause": edge.source,
                    "confidence": edge.confidence,
                    "relationship": edge.relationship
                })
        
        # Also check indirect causes via chains
        for edge in self.edges:
            if edge.target == effect_lower and edge.relationship == "INFLUENCES":
                causes.append({
                    "cause": edge.source,
                    "confidence": edge.confidence * 0.8,  # Discount for indirect
                    "relationship": "INFLUENCES"
                })
        
        return sorted(causes, key=lambda x: x["confidence"], reverse=True)
    
    def query_effects(self, cause: str) -> List[Dict[str, Any]]:
        """What are the effects of this cause?"""
        cause_lower = cause.lower().strip()
        effects = []
        
        for edge in self.edges:
            if edge.source == cause_lower and edge.relationship in ["CAUSES", "LEADS_TO"]:
                effects.append({
                    "effect": edge.target,
                    "confidence": edge.confidence,
                    "relationship": edge.relationship
                })
        
        for edge in self.edges:
            if edge.source == cause_lower and edge.relationship == "INFLUENCES":
                effects.append({
                    "effect": edge.target,
                    "confidence": edge.confidence * 0.8,
                    "relationship": "INFLUENCES"
                })
        
        return sorted(effects, key=lambda x: x["confidence"], reverse=True)
    
    def query_preventions(self, effect: str) -> List[Dict[str, Any]]:
        """What prevents this effect?"""
        effect_lower = effect.lower().strip()
        preventers = []
        
        for edge in self.edges:
            if edge.target == effect_lower and edge.relationship == "PREVENTS":
                preventers.append({
                    "prevents": edge.source,
                    "confidence": edge.confidence
                })
        
        return sorted(preventers, key=lambda x: x["confidence"], reverse=True)
    
    def query_requirements(self, task: str) -> List[Dict[str, Any]]:
        """What is required for this task?"""
        task_lower = task.lower().strip()
        requirements = []
        
        for edge in self.edges:
            if edge.source == task_lower and edge.relationship == "REQUIRES":
                requirements.append({
                    "required": edge.target,
                    "confidence": edge.confidence
                })
        
        return sorted(requirements, key=lambda x: x["confidence"], reverse=True)
    
    def query_contrasts(self, concept: str) -> List[Dict[str, Any]]:
        """What contrasts with this concept?"""
        concept_lower = concept.lower().strip()
        contrasts = []
        
        for edge in self.edges:
            if (edge.source == concept_lower or edge.target == concept_lower) and \
               edge.relationship == "CONTRASTS_WITH":
                other = edge.target if edge.source == concept_lower else edge.source
                contrasts.append({
                    "contrasts_with": other,
                    "confidence": edge.confidence
                })
        
        return contrasts
    
    def query_similar(self, concept: str) -> List[Dict[str, Any]]:
        """What is similar to this concept?"""
        concept_lower = concept.lower().strip()
        similar = []
        
        for edge in self.edges:
            if (edge.source == concept_lower or edge.target == concept_lower) and \
               edge.relationship == "SIMILAR_TO":
                other = edge.target if edge.source == concept_lower else edge.source
                similar.append({
                    "similar_to": other,
                    "confidence": edge.confidence
                })
        
        return similar
    
    def infer_chain(self, start: str, relationship: str = "CAUSES", 
                    max_depth: int = 3) -> List[Dict[str, Any]]:
        """Follow a chain of relationships: A causes B causes C..."""
        start_lower = start.lower().strip()
        chain = []
        visited = {start_lower}
        current = start_lower
        
        for depth in range(max_depth):
            next_concepts = []
            for edge in self.edges:
                if edge.source == current and edge.relationship == relationship:
                    if edge.target not in visited:
                        next_concepts.append({
                            "from": edge.source,
                            "to": edge.target,
                            "relationship": edge.relationship,
                            "confidence": edge.confidence,
                            "depth": depth + 1
                        })
                        visited.add(edge.target)
            
            if not next_concepts:
                break
            
            # Follow the strongest link
            best = max(next_concepts, key=lambda x: x["confidence"])
            chain.append(best)
            current = best["to"]
        
        return chain
    
    def find_contradictions(self) -> List[Tuple[str, str, str]]:
        """Find concepts that have CONTRASTS_WITH edges"""
        contradictions = []
        seen = set()
        
        for edge in self.edges:
            if edge.relationship == "CONTRASTS_WITH":
                pair = tuple(sorted([edge.source, edge.target]))
                if pair not in seen:
                    seen.add(pair)
                    contradictions.append((edge.source, edge.target, "CONTRASTS_WITH"))
        
        return contradictions
    
    def extract_causal_graph(self) -> Dict[str, List[str]]:
        """Extract the causal subgraph as adjacency list"""
        causal = {}
        for edge in self.edges:
            if edge.relationship in ["CAUSES", "LEADS_TO", "INFLUENCES", "PREVENTS"]:
                if edge.source not in causal:
                    causal[edge.source] = []
                causal[edge.source].append({
                    "target": edge.target,
                    "relationship": edge.relationship
                })
        return causal
    
    def get_edge_stats(self) -> Dict[str, int]:
        """Get statistics about edge types"""
        stats = {}
        for edge in self.edges:
            stats[edge.relationship] = stats.get(edge.relationship, 0) + 1
        return stats
    
    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge graph statistics"""
        total_nodes = len(self.nodes)
        total_categories = len(self.categories)
        total_relationships = sum(len(n.related) for n in self.nodes.values())
        total_edges = len(self.edges)
        most_accessed = sorted(self.nodes.values(), key=lambda n: n.access_count, reverse=True)[:5]
        
        return {
            "total_concepts": total_nodes,
            "total_categories": total_categories,
            "total_relationships": total_relationships,
            "total_edges": total_edges,
            "categories_breakdown": {k: len(v) for k, v in self.categories.items()},
            "edge_types": self.get_edge_stats(),
            "most_accessed": [{"concept": n.concept, "access_count": n.access_count} for n in most_accessed]
        }
