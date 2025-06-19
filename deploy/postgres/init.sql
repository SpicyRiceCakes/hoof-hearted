-- 🐎 Hoof Hearted - Database Initialization Script
-- PostgreSQL schema for system monitoring metrics storage

-- Create database and user (if they don't exist)
-- Note: This runs as postgres user during container initialization

-- Ensure extensions are available
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create metrics table for time-series data
CREATE TABLE IF NOT EXISTS metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metric_type VARCHAR(50) NOT NULL,
    value NUMERIC NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    node_id VARCHAR(100) DEFAULT 'default',
    
    -- Indexes for performance
    CONSTRAINT valid_metric_type CHECK (metric_type IN (
        'cpu_usage',
        'cpu_temperature', 
        'gpu_usage',
        'gpu_temperature',
        'gpu_memory',
        'gpu_fan_speed',
        'memory_usage',
        'memory_available',
        'disk_usage',
        'disk_io_read',
        'disk_io_write',
        'network_rx',
        'network_tx',
        'process_cpu',
        'process_memory',
        'process_gpu'
    ))
);

-- Create indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics (timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_metrics_type_timestamp ON metrics (metric_type, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_metrics_node_timestamp ON metrics (node_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_metrics_metadata_gin ON metrics USING GIN (metadata);

-- Create processes table for process monitoring
CREATE TABLE IF NOT EXISTS processes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    pid INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    command_line TEXT,
    cpu_percent NUMERIC DEFAULT 0,
    memory_percent NUMERIC DEFAULT 0,
    gpu_percent NUMERIC DEFAULT 0,
    status VARCHAR(20) DEFAULT 'running',
    created_time TIMESTAMPTZ,
    last_seen TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    node_id VARCHAR(100) DEFAULT 'default',
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Create indexes for process queries
CREATE INDEX IF NOT EXISTS idx_processes_pid ON processes (pid);
CREATE INDEX IF NOT EXISTS idx_processes_name ON processes (name);
CREATE INDEX IF NOT EXISTS idx_processes_last_seen ON processes (last_seen DESC);
CREATE INDEX IF NOT EXISTS idx_processes_node ON processes (node_id);

-- Create alerts table for notification management
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL DEFAULT 'info',
    title VARCHAR(255) NOT NULL,
    message TEXT,
    threshold_value NUMERIC,
    current_value NUMERIC,
    triggered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    node_id VARCHAR(100) DEFAULT 'default',
    metadata JSONB DEFAULT '{}'::jsonb,
    
    CONSTRAINT valid_alert_type CHECK (alert_type IN (
        'cpu_high',
        'gpu_high', 
        'memory_high',
        'temperature_high',
        'disk_full',
        'process_high_usage',
        'system_error'
    )),
    CONSTRAINT valid_severity CHECK (severity IN ('info', 'warning', 'error', 'critical'))
);

-- Create indexes for alert queries
CREATE INDEX IF NOT EXISTS idx_alerts_triggered_at ON alerts (triggered_at DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_active ON alerts (is_active, triggered_at DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_type ON alerts (alert_type);
CREATE INDEX IF NOT EXISTS idx_alerts_node ON alerts (node_id);

-- Create system_info table for node information
CREATE TABLE IF NOT EXISTS system_info (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_id VARCHAR(100) NOT NULL UNIQUE,
    hostname VARCHAR(255),
    platform VARCHAR(100),
    cpu_model VARCHAR(255),
    cpu_cores INTEGER,
    total_memory BIGINT,
    gpu_model VARCHAR(255),
    gpu_memory BIGINT,
    docker_version VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Create index for system info
CREATE INDEX IF NOT EXISTS idx_system_info_node ON system_info (node_id);

-- Create function for automatic updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for system_info updated_at
CREATE TRIGGER update_system_info_updated_at 
    BEFORE UPDATE ON system_info 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Create data retention function
CREATE OR REPLACE FUNCTION cleanup_old_metrics(retention_days INTEGER DEFAULT 30)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM metrics 
    WHERE timestamp < NOW() - INTERVAL '1 day' * retention_days;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    
    -- Log cleanup operation
    INSERT INTO alerts (alert_type, severity, title, message, metadata)
    VALUES (
        'system_error',
        'info',
        'Metrics Cleanup',
        format('Cleaned up %s old metric records older than %s days', deleted_count, retention_days),
        jsonb_build_object('deleted_count', deleted_count, 'retention_days', retention_days)
    );
    
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Create function to resolve old alerts
CREATE OR REPLACE FUNCTION resolve_old_alerts(resolution_hours INTEGER DEFAULT 24)
RETURNS INTEGER AS $$
DECLARE
    resolved_count INTEGER;
BEGIN
    UPDATE alerts 
    SET is_active = FALSE, resolved_at = NOW()
    WHERE is_active = TRUE 
    AND triggered_at < NOW() - INTERVAL '1 hour' * resolution_hours;
    
    GET DIAGNOSTICS resolved_count = ROW_COUNT;
    RETURN resolved_count;
END;
$$ LANGUAGE plpgsql;

-- Create sample configuration table
CREATE TABLE IF NOT EXISTS config (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key VARCHAR(100) NOT NULL UNIQUE,
    value TEXT,
    value_type VARCHAR(20) DEFAULT 'string',
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT valid_value_type CHECK (value_type IN ('string', 'integer', 'float', 'boolean', 'json'))
);

-- Create trigger for config updated_at
CREATE TRIGGER update_config_updated_at 
    BEFORE UPDATE ON config 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert default configuration
INSERT INTO config (key, value, value_type, description) VALUES
    ('metrics_retention_days', '30', 'integer', 'Number of days to retain metrics data'),
    ('alerts_resolution_hours', '24', 'integer', 'Hours after which to auto-resolve alerts'),
    ('cpu_alert_threshold', '80', 'float', 'CPU usage percentage to trigger alerts'),
    ('gpu_alert_threshold', '85', 'float', 'GPU usage percentage to trigger alerts'),
    ('memory_alert_threshold', '90', 'float', 'Memory usage percentage to trigger alerts'),
    ('temperature_alert_threshold', '75', 'float', 'Temperature in Celsius to trigger alerts'),
    ('metrics_interval', '5', 'integer', 'Metrics collection interval in seconds'),
    ('enable_gpu_monitoring', 'true', 'boolean', 'Enable GPU monitoring'),
    ('enable_process_monitoring', 'true', 'boolean', 'Enable process monitoring'),
    ('dashboard_refresh_interval', '5', 'integer', 'Dashboard refresh interval in seconds')
ON CONFLICT (key) DO NOTHING;

-- Create initial system info record
INSERT INTO system_info (node_id, hostname) VALUES ('default', 'hoof-hearted-server')
ON CONFLICT (node_id) DO NOTHING;

-- Grant permissions (assuming the user exists)
-- Note: User creation happens in docker-compose environment variables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hoof_hearted;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hoof_hearted;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO hoof_hearted;

-- Create view for latest metrics
CREATE OR REPLACE VIEW latest_metrics AS
SELECT DISTINCT ON (metric_type, node_id)
    metric_type,
    value,
    timestamp,
    metadata,
    node_id
FROM metrics
ORDER BY metric_type, node_id, timestamp DESC;

-- Create view for active alerts
CREATE OR REPLACE VIEW active_alerts AS
SELECT *
FROM alerts
WHERE is_active = TRUE
ORDER BY triggered_at DESC;

-- Create view for system overview
CREATE OR REPLACE VIEW system_overview AS
SELECT
    si.node_id,
    si.hostname,
    si.platform,
    si.cpu_model,
    si.cpu_cores,
    si.total_memory,
    si.gpu_model,
    si.gpu_memory,
    (SELECT COUNT(*) FROM active_alerts WHERE node_id = si.node_id) as active_alerts_count,
    (SELECT MAX(timestamp) FROM metrics WHERE node_id = si.node_id) as last_metric_time
FROM system_info si;

-- Log successful initialization
INSERT INTO alerts (alert_type, severity, title, message, metadata)
VALUES (
    'system_error',
    'info', 
    'Database Initialized',
    'Hoof Hearted database schema created successfully',
    jsonb_build_object(
        'version', '1.0',
        'initialized_at', NOW(),
        'tables_created', ARRAY['metrics', 'processes', 'alerts', 'system_info', 'config']
    )
);

-- Display initialization summary
DO $$
BEGIN
    RAISE NOTICE '🐎 Hoof Hearted Database Initialized Successfully!';
    RAISE NOTICE '📊 Tables: metrics, processes, alerts, system_info, config';
    RAISE NOTICE '🔍 Views: latest_metrics, active_alerts, system_overview';
    RAISE NOTICE '⚙️ Functions: cleanup_old_metrics(), resolve_old_alerts()';
    RAISE NOTICE '🌶️ SpicyRiceCakes - Making dreams reality!';
END $$;