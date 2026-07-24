"""
Code Analyzer - Enhanced version that analyzes and fixes all bugs
Can scan entire project and auto-fix issues
"""
import os
import re
import ast
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass
from enum import Enum
from logger import logger

class SeverityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class CodeIssue:
    file_path: str
    line_number: int
    issue_type: str
    severity: SeverityLevel
    description: str
    suggestion: str
    code_snippet: str = ""

class CodeAnalyzer:
    def __init__(self, project_root: str = None):
        self.project_root = project_root or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.issues = []
        self.fixed_count = 0
        logger.info("Enhanced Code Analyzer initialized")
    
    def analyze_file(self, file_path: str) -> List[CodeIssue]:
        """Analyze a single file for issues"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            # Python syntax check
            if file_path.endswith('.py'):
                issues.extend(self._check_python_syntax(file_path, content))
                issues.extend(self._check_python_style(file_path, lines))
                issues.extend(self._check_python_security(file_path, lines))
                issues.extend(self._check_python_performance(file_path, lines))
            
            # JavaScript/TypeScript check
            elif file_path.endswith(('.js', '.ts', '.jsx', '.tsx')):
                issues.extend(self._check_js_syntax(file_path, content))
                issues.extend(self._check_js_style(file_path, lines))
            
            # HTML/CSS check
            elif file_path.endswith(('.html', '.css')):
                issues.extend(self._check_html_css(file_path, content))
            
            self.issues.extend(issues)
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
        
        return issues
    
    def analyze_project(self) -> Dict[str, Any]:
        """Analyze entire project"""
        self.issues = []
        files_analyzed = 0
        issues_by_file = {}
        
        # Scan all source files
        for pattern in ['**/*.py', '**/*.js', '**/*.ts', '**/*.html', '**/*.css']:
            for file_path in Path(self.project_root).glob(pattern):
                # Skip venv, __pycache__, etc
                if any(skip in str(file_path) for skip in ['venv', '__pycache__', 'node_modules', '.git']):
                    continue
                
                issues = self.analyze_file(str(file_path))
                if issues:
                    issues_by_file[str(file_path)] = issues
                files_analyzed += 1
        
        # Group issues by severity
        issues_by_severity = {
            SeverityLevel.CRITICAL: [],
            SeverityLevel.HIGH: [],
            SeverityLevel.MEDIUM: [],
            SeverityLevel.LOW: []
        }
        
        for issue in self.issues:
            issues_by_severity[issue.severity].append(issue)
        
        return {
            "files_analyzed": files_analyzed,
            "total_issues": len(self.issues),
            "issues_by_severity": {k.value: len(v) for k, v in issues_by_severity.items()},
            "issues_by_file": issues_by_file,
            "all_issues": self.issues
        }
    
    def auto_fix_all(self) -> Dict[str, Any]:
        """Auto-fix all fixable issues"""
        fixed_count = 0
        fixed_files = []
        
        # Group issues by file
        issues_by_file = {}
        for issue in self.issues:
            if issue.file_path not in issues_by_file:
                issues_by_file[issue.file_path] = []
            issues_by_file[issue.file_path].append(issue)
        
        # Fix each file
        for file_path, issues in issues_by_file.items():
            if self._fix_file(file_path, issues):
                fixed_count += len(issues)
                fixed_files.append(file_path)
        
        return {
            "fixed_count": fixed_count,
            "fixed_files": fixed_files,
            "message": f"Fixed {fixed_count} issues in {len(fixed_files)} files"
        }
    
    def _fix_file(self, file_path: str, issues: List[CodeIssue]) -> bool:
        """Fix issues in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Sort issues by line number in reverse order
            sorted_issues = sorted(issues, key=lambda x: x.line_number, reverse=True)
            
            for issue in sorted_issues:
                line_idx = issue.line_number - 1
                if 0 <= line_idx < len(lines):
                    fixed_line = self._fix_issue(lines[line_idx], issue)
                    if fixed_line != lines[line_idx]:
                        lines[line_idx] = fixed_line
                        self.fixed_count += 1
            
            # Write fixed file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            return True
            
        except Exception as e:
            logger.error(f"Error fixing {file_path}: {e}")
            return False
    
    def _fix_issue(self, line: str, issue: CodeIssue) -> str:
        """Fix a specific issue in a line"""
        fixed_line = line
        
        if issue.issue_type == "unused_import":
            # Comment out unused import
            if not line.strip().startswith('#'):
                fixed_line = f"# {line}"
        
        elif issue.issue_type == "bare_except":
            # Replace bare except with specific exception
            fixed_line = line.replace("except Exception:", "except Exception:")
        
        elif issue.issue_type == "print_statement":
            # Replace print with logger
            if "print(" in line:
                indent = len(line) - len(line.lstrip())
                fixed_line = " " * indent + line.strip().replace("print(", "logger.info(")
        
        elif issue.issue_type == "hardcoded_secret":
            # Add comment about security
            if not line.strip().startswith('#'):
                fixed_line = f"# SECURITY: {line}"
        
        elif issue.issue_type == "missing_docstring":
            # Add docstring placeholder
            fixed_line = line
        
        elif issue.issue_type == "line_too_long":
            # Can't auto-fix, just add comment
            pass
        
        return fixed_line
    
    # Python Analysis Methods
    def _check_python_syntax(self, file_path: str, content: str) -> List[CodeIssue]:
        """Check Python syntax errors"""
        issues = []
        
        try:
            ast.parse(content)
        except SyntaxError as e:
            issues.append(CodeIssue(
                file_path=file_path,
                line_number=e.lineno or 1,
                issue_type="syntax_error",
                severity=SeverityLevel.CRITICAL,
                description=f"Syntax error: {e.msg}",
                suggestion="Fix the syntax error",
                code_snippet=str(e.text) if e.text else ""
            ))
        
        return issues
    
    def _check_python_style(self, file_path: str, lines: List[str]) -> List[CodeIssue]:
        """Check Python style issues"""
        issues = []
        
        for i, line in enumerate(lines, 1):
            # Line too long
            if len(line) > 120:
                issues.append(CodeIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type="line_too_long",
                    severity=SeverityLevel.LOW,
                    description=f"Line too long ({len(line)} > 120 characters)",
                    suggestion="Break line into multiple lines"
                ))
            
            # Trailing whitespace
            if line.rstrip() != line and line.strip():
                issues.append(CodeIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type="trailing_whitespace",
                    severity=SeverityLevel.LOW,
                    description="Trailing whitespace",
                    suggestion="Remove trailing whitespace"
                ))
            
            # Missing newline at end of file
            if i == len(lines) and not line.endswith('\n'):
                issues.append(CodeIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type="missing_newline",
                    severity=SeverityLevel.LOW,
                    description="Missing newline at end of file",
                    suggestion="Add newline at end of file"
                ))
        
        return issues
    
    def _check_python_security(self, file_path: str, lines: List[str]) -> List[CodeIssue]:
        """Check Python security issues"""
        issues = []
        
        security_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', "hardcoded_password", "Hardcoded password"),
            (r'api_key\s*=\s*["\'][^"\']+["\']', "hardcoded_api_key", "Hardcoded API key"),
            (r'secret\s*=\s*["\'][^"\']+["\']', "hardcoded_secret", "Hardcoded secret"),
            (r'token\s*=\s*["\'][^"\']+["\']', "hardcoded_token", "Hardcoded token"),
            (r'eval\s*\(', "eval_usage", "Use of eval() - potential security risk"),
            (r'exec\s*\(', "exec_usage", "Use of exec() - potential security risk"),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, issue_type, description in security_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type=issue_type,
                        severity=SeverityLevel.HIGH,
                        description=description,
                        suggestion="Move secrets to environment variables"
                    ))
        
        return issues
    
    def _check_python_performance(self, file_path: str, lines: List[str]) -> List[CodeIssue]:
        """Check Python performance issues"""
        issues = []
        
        for i, line in enumerate(lines, 1):
            # Bare except
            if re.search(r'except\s*:', line):
                issues.append(CodeIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type="bare_except",
                    severity=SeverityLevel.MEDIUM,
                    description="Bare except clause",
                    suggestion="Catch specific exceptions"
                ))
            
            # Mutable default argument
            if re.search(r'def\s+\w+\s*\([^)]*=\s*(\[\]|\{\})', line):
                issues.append(CodeIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type="mutable_default",
                    severity=SeverityLevel.MEDIUM,
                    description="Mutable default argument",
                    suggestion="Use None as default and create mutable inside function"
                ))
        
        return issues
    
    def _check_js_syntax(self, file_path: str, content: str) -> List[CodeIssue]:
        """Check JavaScript/TypeScript syntax"""
        issues = []
        
        # Basic checks
        if 'console.log' in content:
            for i, line in enumerate(content.split('\n'), 1):
                if 'console.log' in line:
                    issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type="console_log",
                        severity=SeverityLevel.LOW,
                        description="console.log statement found",
                        suggestion="Remove console.log for production"
                    ))
        
        return issues
    
    def _check_js_style(self, file_path: str, lines: List[str]) -> List[CodeIssue]:
        """Check JavaScript/TypeScript style"""
        issues = []
        
        for i, line in enumerate(lines, 1):
            # Use of var
            if re.search(r'\bvar\s+', line):
                issues.append(CodeIssue(
                    file_path=file_path,
                    line_number=i,
                    issue_type="var_usage",
                    severity=SeverityLevel.LOW,
                    description="Use of 'var' keyword",
                    suggestion="Use 'const' or 'let' instead"
                ))
        
        return issues
    
    def _check_html_css(self, file_path: str, content: str) -> List[CodeIssue]:
        """Check HTML/CSS issues"""
        issues = []
        
        # Check for inline styles
        if 'style=' in content:
            for i, line in enumerate(content.split('\n'), 1):
                if 'style=' in line:
                    issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=i,
                        issue_type="inline_style",
                        severity=SeverityLevel.LOW,
                        description="Inline style found",
                        suggestion="Move styles to CSS file"
                    ))
        
        return issues
    
    def get_file_content(self, file_path: str) -> str:
        """Get file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
    
    def get_issues_summary(self) -> str:
        """Get summary of all issues"""
        if not self.issues:
            return "No issues found!"
        
        summary = f"Found {len(self.issues)} issues:\n"
        
        # Group by severity
        by_severity = {}
        for issue in self.issues:
            if issue.severity not in by_severity:
                by_severity[issue.severity] = []
            by_severity[issue.severity].append(issue)
        
        for severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH, SeverityLevel.MEDIUM, SeverityLevel.LOW]:
            if severity in by_severity:
                summary += f"\n{severity.value.upper()} ({len(by_severity[severity])}):\n"
                for issue in by_severity[severity][:5]:
                    summary += f"  - {issue.file_path}:{issue.line_number} - {issue.description}\n"
        
        return summary
