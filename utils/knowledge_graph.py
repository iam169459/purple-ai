"""
Knowledge Graph
Structured knowledge representation with relationships
"""
import json
import os
import time
from typing import Dict, Any, List, Optional, Set
from logger import logger

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
        self._load()
        logger.info(f"🧠 Knowledge Graph initialized | {len(self.nodes)} concepts loaded")
    
    def _load(self):
        """Load knowledge graph from disk"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for concept, node_data in data.get("nodes", {}).items():
                        self.nodes[concept] = KnowledgeNode.from_dict(node_data)
                    self.categories = {k: set(v) for k, v in data.get("categories", {}).items()}
                logger.info(f"📚 Loaded {len(self.nodes)} knowledge nodes")
        except Exception as e:
            logger.error(f"Error loading knowledge graph: {e}")
            self.nodes = {}
            self.categories = {}
    
    def save(self):
        """Save knowledge graph to disk"""
        try:
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            data = {
                "nodes": {c: n.to_dict() for c, n in self.nodes.items()},
                "categories": {k: list(v) for k, v in self.categories.items()},
                "saved_at": time.time()
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"💾 Knowledge graph saved: {len(self.nodes)} nodes")
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
    
    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge graph statistics"""
        total_nodes = len(self.nodes)
        total_categories = len(self.categories)
        total_relationships = sum(len(n.related) for n in self.nodes.values())
        most_accessed = sorted(self.nodes.values(), key=lambda n: n.access_count, reverse=True)[:5]
        
        return {
            "total_concepts": total_nodes,
            "total_categories": total_categories,
            "total_relationships": total_relationships,
            "categories_breakdown": {k: len(v) for k, v in self.categories.items()},
            "most_accessed": [{"concept": n.concept, "access_count": n.access_count} for n in most_accessed]
        }
    
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
            "",
            "Categories:",
        ]
        for cat, count in stats['categories_breakdown'].items():
            lines.append(f"  • {cat}: {count} concepts")
        
        lines.append("")
        lines.append("Most Accessed Concepts:")
        for item in stats['most_accessed']:
            lines.append(f"  • {item['concept']}: {item['access_count']} accesses")
        
        lines.append("=" * 50)
        return "\n".join(lines)
