package th.co.scb.ace.demo.recovery.casewf.config;

import org.springframework.transaction.TransactionDefinition;
import org.springframework.transaction.support.AbstractPlatformTransactionManager;
import org.springframework.transaction.support.DefaultTransactionStatus;

/**
 * A transaction manager that runs {@code doBegin}, {@code doCommit} and {@code doRollback} without a
 * resource, so a real {@code TransactionTemplate} executes its callback in a unit test. No new
 * dependency (TASK-18).
 */
class StubTransactionManager extends AbstractPlatformTransactionManager {

	@Override
	protected Object doGetTransaction() {
		return new Object();
	}

	@Override
	protected void doBegin(Object transaction, TransactionDefinition definition) {
	}

	@Override
	protected void doCommit(DefaultTransactionStatus status) {
	}

	@Override
	protected void doRollback(DefaultTransactionStatus status) {
	}
}