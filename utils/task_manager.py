"""
Task Manager
Handles task decomposition, delegation, queueing, and result aggregation
"""
import uuid
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from logger import logger

@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: str = ""
    description: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    priority: int = 3  # 1=urgent, 5=low
    parent_id: Optional[str] = None
    subtasks: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, queued, assigned, working, completed, failed
    result: Optional[Dict[str, Any]] = None
    assigned_agent: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None

class TaskManager:
    """Manages the lifecycle of tasks in the agent swarm"""
    
    def __init__(self):
        self.tasks = {}  # task_id -> Task
        self.queue = []  # Ordered list of pending task IDs
        self.completed_results = []
        logger.info("📋 Task Manager initialized")
    
    def create_task(self, task_type: str, description: str, payload: Dict[str, Any] = None, 
                    priority: int = 3, parent_id: Optional[str] = None) -> Task:
        """Create a new task"""
        task = Task(
            type=task_type,
            description=description,
            payload=payload or {},
            priority=priority,
            parent_id=parent_id
        )
        self.tasks[task.id] = task
        self._enqueue(task.id)
        logger.info(f"📝 Task created: [{task_type}] {description}")
        return task
    
    def decompose_task(self, parent_task: Task, subtask_specs: List[Dict[str, Any]]) -> List[Task]:
        """Break a complex task into subtasks"""
        subtasks = []
        for spec in subtask_specs:
            subtask = self.create_task(
                task_type=spec.get("type", "generic"),
                description=spec.get("description", "Subtask"),
                payload=spec.get("payload", {}),
                priority=parent_task.priority,
                parent_id=parent_task.id
            )
            subtasks.append(subtask)
            parent_task.subtasks.append(subtask.id)
        
        logger.info(f"🔨 Task '{parent_task.description}' decomposed into {len(subtasks)} subtasks")
        return subtasks
    
    def get_next_task(self, agent_expertise: List[str]) -> Optional[Task]:
        """Get the next available task matching agent expertise"""
        for task_id in self.queue:
            task = self.tasks[task_id]
            if task.status == "pending" and self._can_agent_handle(agent_expertise, task.type):
                # Check dependencies
                if all(self.tasks[dep].status == "completed" for dep in task.dependencies if dep in self.tasks):
                    task.status = "assigned"
                    return task
        return None
    
    def _can_agent_handle(self, expertise: List[str], task_type: str) -> bool:
        """Check if agent expertise matches task type"""
        return task_type.lower() in [e.lower() for e in expertise]
    
    def _enqueue(self, task_id: str):
        """Add task to queue sorted by priority"""
        self.queue.append(task_id)
        self.queue.sort(key=lambda tid: self.tasks[tid].priority)
    
    def complete_task(self, task_id: str, result: Dict[str, Any]):
        """Mark a task as completed with results"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = "completed"
            task.result = result
            task.completed_at = time.time()
            self.completed_results.append({
                "task_id": task_id,
                "type": task.type,
                "description": task.description,
                "result": result,
                "duration": round(task.completed_at - task.created_at, 2) if task.completed_at else 0
            })
            
            # Check if parent task is complete
            if task.parent_id and task.parent_id in self.tasks:
                self._check_parent_completion(task.parent_id)
            
            logger.info(f"✅ Task '{task.description}' completed")
    
    def _check_parent_completion(self, parent_id: str):
        """Check if all subtasks of a parent are done"""
        parent = self.tasks[parent_id]
        if parent.subtasks and all(self.tasks[sid].status == "completed" for sid in parent.subtasks if sid in self.tasks):
            # Aggregate subtask results
            results = [self.tasks[sid].result for sid in parent.subtasks if sid in self.tasks]
            parent.status = "completed"
            parent.result = {
                "aggregated": True,
                "subtask_results": results,
                "summary": self._summarize_results(results)
            }
            logger.info(f"📦 Parent task '{parent.description}' auto-completed with {len(results)} sub-results")
    
    def _summarize_results(self, results: List[Dict]) -> str:
        """Create a simple summary of multiple results"""
        successful = [r for r in results if r and r.get("success", False)]
        return f"Completed {len(successful)}/{len(results)} subtasks successfully"
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            return {
                "id": task.id,
                "type": task.type,
                "description": task.description,
                "status": task.status,
                "assigned_agent": task.assigned_agent,
                "has_result": task.result is not None
            }
        return None
    
    def get_all_pending(self) -> List[Task]:
        """Get all pending tasks"""
        return [self.tasks[tid] for tid in self.queue if self.tasks[tid].status == "pending"]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get task manager statistics"""
        statuses = {"pending": 0, "queued": 0, "assigned": 0, "working": 0, "completed": 0, "failed": 0}
        for task in self.tasks.values():
            statuses[task.status] = statuses.get(task.status, 0) + 1
        return {
            "total_tasks": len(self.tasks),
            "pending": statuses.get("pending", 0),
            "completed": statuses.get("completed", 0),
            "failed": statuses.get("failed", 0),
            "queue_length": len(self.queue)
        }
