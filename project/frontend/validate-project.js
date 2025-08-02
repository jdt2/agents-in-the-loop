#!/usr/bin/env node

/**
 * Frontend Validation Script
 * Tests core functionality of the React TypeScript Todo Application
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

console.log('🔍 Frontend Project Validation Script');
console.log('=====================================\n');

const results = {
  passed: 0,
  failed: 0,
  warnings: 0,
  tests: []
};

function test(name, testFn) {
  try {
    console.log(`⏳ Testing: ${name}`);
    const result = testFn();
    if (result === true) {
      console.log(`✅ PASS: ${name}\n`);
      results.passed++;
      results.tests.push({ name, status: 'PASS', message: '' });
    } else if (result && result.warning) {
      console.log(`⚠️ WARNING: ${name} - ${result.message}\n`);
      results.warnings++;
      results.tests.push({ name, status: 'WARNING', message: result.message });
    } else {
      const message = result && result.message ? result.message : 'Test failed';
      console.log(`❌ FAIL: ${name} - ${message}\n`);
      results.failed++;
      results.tests.push({ name, status: 'FAIL', message });
    }
  } catch (error) {
    console.log(`❌ FAIL: ${name} - ${error.message}\n`);
    results.failed++;
    results.tests.push({ name, status: 'FAIL', message: error.message });
  }
}

// Test 1: Package.json validation
test('Package.json structure and dependencies', () => {
  const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  
  if (!pkg.dependencies || !pkg.dependencies.react || !pkg.dependencies['react-dom']) {
    return { message: 'Missing required React dependencies' };
  }
  
  if (!pkg.devDependencies || !pkg.devDependencies.typescript || !pkg.devDependencies.vite) {
    return { message: 'Missing required dev dependencies (TypeScript, Vite)' };
  }
  
  if (!pkg.scripts || !pkg.scripts.dev || !pkg.scripts.build) {
    return { message: 'Missing required npm scripts (dev, build)' };
  }
  
  return true;
});

// Test 2: TypeScript configuration
test('TypeScript configuration', () => {
  if (!fs.existsSync('tsconfig.json')) {
    return { message: 'tsconfig.json not found' };
  }
  
  try {
    // Test TypeScript compilation instead of parsing JSON with comments
    execSync('npx tsc --showConfig', { stdio: 'pipe' });
    
    // Check if file contains key configurations
    const tsconfigContent = fs.readFileSync('tsconfig.json', 'utf8');
    
    if (!tsconfigContent.includes('"strict": true')) {
      return { message: 'TypeScript strict mode not enabled' };
    }
    
    if (!tsconfigContent.includes('"include"') || !tsconfigContent.includes('src')) {
      return { message: 'TypeScript not configured to include src directory' };
    }
    
    return true;
  } catch (error) {
    return { message: 'TypeScript configuration is invalid' };
  }
});

// Test 3: Required source files exist
test('Required source files structure', () => {
  const requiredFiles = [
    'src/main.tsx',
    'src/App.tsx',
    'src/components/TodoApp.tsx',
    'src/components/TodoList.tsx',
    'src/components/TodoItem.tsx',
    'src/components/TodoForm.tsx',
    'src/components/FilterButtons.tsx',
    'src/components/TodoCounter.tsx',
    'src/types/todo.ts',
    'src/services/todoService.ts',
    'src/hooks/useTodos.ts',
    'src/index.css'
  ];
  
  const missingFiles = requiredFiles.filter(file => !fs.existsSync(file));
  
  if (missingFiles.length > 0) {
    return { message: `Missing files: ${missingFiles.join(', ')}` };
  }
  
  return true;
});

// Test 4: TypeScript compilation
test('TypeScript compilation check', () => {
  try {
    execSync('npx tsc --noEmit', { stdio: 'pipe' });
    return true;
  } catch (error) {
    return { message: 'TypeScript compilation failed' };
  }
});

// Test 5: Build process
test('Production build', () => {
  try {
    execSync('npm run build', { stdio: 'pipe' });
    
    if (!fs.existsSync('dist/index.html') || !fs.existsSync('dist/assets')) {
      return { message: 'Build artifacts not found in dist directory' };
    }
    
    return true;
  } catch (error) {
    return { message: 'Build process failed' };
  }
});

// Test 6: API configuration
test('API configuration', () => {
  const serviceFile = fs.readFileSync('src/services/todoService.ts', 'utf8');
  
  if (!serviceFile.includes('http://localhost:8000/api')) {
    return { message: 'API base URL not correctly configured for backend port 8000' };
  }
  
  if (!serviceFile.includes('getAllTodos') || !serviceFile.includes('createTodo') || !serviceFile.includes('updateTodo') || !serviceFile.includes('deleteTodo')) {
    return { message: 'Missing required API service methods' };
  }
  
  return true;
});

// Test 7: Component structure validation
test('Component exports and imports', () => {
  const appFile = fs.readFileSync('src/App.tsx', 'utf8');
  const todoAppFile = fs.readFileSync('src/components/TodoApp.tsx', 'utf8');
  
  if (!appFile.includes('TodoApp')) {
    return { message: 'App.tsx does not import TodoApp component' };
  }
  
  if (!todoAppFile.includes('useTodos')) {
    return { message: 'TodoApp does not use the useTodos hook' };
  }
  
  return true;
});

// Test 8: Styling configuration
test('Styling and CSS setup', () => {
  if (!fs.existsSync('tailwind.config.js')) {
    return { message: 'Tailwind CSS configuration not found' };
  }
  
  if (!fs.existsSync('postcss.config.js')) {
    return { message: 'PostCSS configuration not found' };
  }
  
  if (!fs.existsSync('src/index.css')) {
    return { message: 'Main CSS file not found' };
  }
  
  return true;
});

// Test 9: Security vulnerability check
test('Security vulnerabilities', () => {
  try {
    const output = execSync('npm audit --audit-level moderate', { stdio: 'pipe', encoding: 'utf8' });
    if (output.includes('vulnerabilities')) {
      return { warning: true, message: 'Security vulnerabilities found in dependencies' };
    }
    return true;
  } catch (error) {
    // npm audit returns non-zero exit code when vulnerabilities are found
    return { warning: true, message: 'Security vulnerabilities detected in dependencies' };
  }
});

// Test 10: Port configuration
test('Development server port configuration', () => {
  const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  
  if (!pkg.scripts.dev.includes('--port 3000')) {
    return { message: 'Development server not configured to run on port 3000' };
  }
  
  return true;
});

// Generate report
console.log('\n📊 VALIDATION RESULTS');
console.log('=====================');
console.log(`✅ Passed: ${results.passed}`);
console.log(`⚠️ Warnings: ${results.warnings}`);
console.log(`❌ Failed: ${results.failed}`);
console.log(`📝 Total Tests: ${results.tests.length}\n`);

if (results.failed > 0) {
  console.log('❌ CRITICAL ISSUES:');
  results.tests.filter(t => t.status === 'FAIL').forEach(test => {
    console.log(`   • ${test.name}: ${test.message}`);
  });
  console.log('');
}

if (results.warnings > 0) {
  console.log('⚠️ WARNINGS:');
  results.tests.filter(t => t.status === 'WARNING').forEach(test => {
    console.log(`   • ${test.name}: ${test.message}`);
  });
  console.log('');
}

const score = ((results.passed + results.warnings * 0.5) / results.tests.length * 100).toFixed(1);
console.log(`🎯 Overall Score: ${score}%`);

if (results.failed === 0) {
  console.log('🎉 Frontend validation completed successfully!');
  console.log('✨ Your Todo application is ready for development and testing.');
} else {
  console.log('🔧 Please fix the critical issues before proceeding.');
  process.exit(1);
}