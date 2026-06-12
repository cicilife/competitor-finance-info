import React, { useState } from 'react';
import { dataComments, DataComment } from '../data/comments';

interface DataMarkerProps {
  companyId: string;
  metric: string;
  year?: string;
  children: React.ReactNode;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left';
}

// 图标样式 - 使用SVG图标替代emoji
const InfoIcon = () => (
  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="10" />
    <line x1="12" y1="16" x2="12" y2="12" />
    <line x1="12" y1="8" x2="12.01" y2="8" />
  </svg>
);

const ExternalLinkIcon = () => (
  <svg className="w-3 h-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
    <polyline points="15 3 21 3 21 9" />
    <line x1="10" y1="14" x2="21" y2="3" />
  </svg>
);

export function DataMarker({ companyId, metric, year, children, position = 'top-right' }: DataMarkerProps) {
  const [isHovered, setIsHovered] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);

  // 获取匹配的注释
  const comments = dataComments.filter(c =>
    (c.companyId === companyId || companyId === 'all') &&
    (c.metric === metric || metric === 'all') &&
    (!year || c.year === year || c.year === '2025')
  );

  if (comments.length === 0) {
    return <>{children}</>;
  }

  const getPositionClasses = () => {
    switch (position) {
      case 'top-left':
        return 'bottom-full left-0 mb-2';
      case 'bottom-right':
        return 'top-full right-0 mt-2';
      case 'bottom-left':
        return 'top-full left-0 mt-2';
      default:
        return 'bottom-full right-0 mb-2';
    }
  };

  return (
    <div
      className="relative inline-flex items-center"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {children}
      <button
        className="ml-1 p-0.5 rounded-full bg-amber-100 text-amber-600 hover:bg-amber-200 transition-colors cursor-pointer"
        onClick={() => setShowTooltip(!showTooltip)}
        title="查看数据注释"
      >
        <InfoIcon />
      </button>

      {/* 悬停提示 */}
      {isHovered && !showTooltip && (
        <div className={`absolute ${getPositionClasses()} z-50 w-64 bg-gray-900 text-white rounded-lg shadow-xl p-3 text-sm`}>
          <div className="text-xs text-gray-400 mb-1">点击查看详情</div>
          <div className="text-amber-400 font-medium">
            有 {comments.length} 条相关注释
          </div>
        </div>
      )}

      {/* 详细弹窗 */}
      {showTooltip && (
        <div className={`absolute ${getPositionClasses()} z-50 w-80 bg-white rounded-xl shadow-2xl border border-gray-200 overflow-hidden`}>
          {/* 标题栏 */}
          <div className="bg-gradient-to-r from-amber-500 to-orange-500 px-4 py-3 flex justify-between items-center">
            <span className="text-white font-semibold">数据注释</span>
            <button
              onClick={() => setShowTooltip(false)}
              className="text-white hover:bg-white/20 rounded p-1"
            >
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          {/* 注释列表 */}
          <div className="max-h-64 overflow-y-auto p-3 space-y-3">
            {comments.map((comment) => (
              <div
                key={comment.id}
                className="bg-gray-50 rounded-lg p-3 border border-gray-100 hover:border-amber-200 transition-colors"
              >
                <div className="flex items-start gap-2">
                  <div className="flex-1">
                    <div className="text-sm text-gray-800 leading-relaxed">
                      {comment.comment}
                    </div>
                    <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
                      <span className="bg-gray-200 px-2 py-0.5 rounded">{comment.year}</span>
                      <span>{comment.source}</span>
                    </div>
                  </div>
                  {comment.url && (
                    <a
                      href={comment.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-1 text-blue-600 hover:text-blue-800 text-xs px-2 py-1 rounded bg-blue-50 hover:bg-blue-100 transition-colors"
                    >
                      <ExternalLinkIcon />
                      <span>查看</span>
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>

          {/* 底部提示 */}
          <div className="bg-gray-50 px-4 py-2 text-xs text-gray-500 border-t">
            数据来源: 行业研究报告、公司年报、投资者关系披露
          </div>
        </div>
      )}
    </div>
  );
}

// 简化的内联标记组件 - 用于表格数据
interface InlineCommentProps {
  companyId: string;
  metric: string;
  value: string | number;
  year?: string;
}

export function InlineCommentMarker({ companyId, metric, value, year }: InlineCommentProps) {
  const comments = dataComments.filter(c =>
    (c.companyId === companyId || companyId === 'all') &&
    (c.metric === metric || metric === 'all')
  );

  if (comments.length === 0) {
    return <span>{value}</span>;
  }

  return (
    <DataMarker companyId={companyId} metric={metric} year={year}>
      <span className="cursor-help border-b border-dashed border-amber-400">{value}</span>
    </DataMarker>
  );
}

// 品牌对比卡片中的注释标记
interface CardCommentProps {
  companyId: string;
  metric: string;
  label: string;
  value: string | number;
  year?: string;
}

export function CardCommentMarker({ companyId, metric, label, value, year }: CardCommentProps) {
  const comments = dataComments.filter(c =>
    (c.companyId === companyId || companyId === 'all') &&
    (c.metric === metric || metric === 'all')
  );

  return (
    <div className="flex items-center gap-2">
      <span className={`${comments.length > 0 ? 'cursor-help' : ''}`}>
        <span className="text-sm text-gray-500">{label}</span>
        <span className={`text-xl font-semibold ml-1 ${comments.length > 0 ? 'text-gray-900' : 'text-gray-900'}`}>
          {value}
        </span>
        {comments.length > 0 && (
          <span className="ml-1 text-amber-500 text-xs">*</span>
        )}
      </span>
      {comments.length > 0 && (
        <DataMarker companyId={companyId} metric={metric} year={year} position="top-left">
          <span />
        </DataMarker>
      )}
    </div>
  );
}

// 图表数据点的注释组件
interface ChartPointCommentProps {
  companyId: string;
  metric: string;
  year: string;
  children: React.ReactNode;
}

export function ChartPointMarker({ companyId, metric, year, children }: ChartPointCommentProps) {
  const comments = dataComments.filter(c =>
    (c.companyId === companyId || companyId === 'all') &&
    (c.metric === metric || metric === 'all')
  );

  if (comments.length === 0) {
    return <>{children}</>;
  }

  return (
    <div className="relative group">
      {children}
      <DataMarker companyId={companyId} metric={metric} year={year} position="top-left">
        <span className="absolute -top-1 -right-1 w-4 h-4 bg-amber-400 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity" />
      </DataMarker>
    </div>
  );
}

// 趋势数据的注释标记
interface TrendMarkerProps {
  companyId: string;
  metric: string;
  period: string;
  children: React.ReactNode;
}

export function TrendPointMarker({ companyId, metric, period, children }: TrendMarkerProps) {
  const comments = dataComments.filter(c =>
    (c.companyId === companyId || companyId === 'all') &&
    (c.metric === metric || c.metric === 'all')
  );

  if (comments.length === 0) {
    return <>{children}</>;
  }

  return (
    <div className="relative">
      {children}
      <DataMarker companyId={companyId} metric={metric} position="bottom-right">
        <span className="absolute -bottom-1 -right-1 w-4 h-4 bg-amber-400 rounded-full flex items-center justify-center text-xs font-bold text-white shadow">
          {comments.length}
        </span>
      </DataMarker>
    </div>
  );
}

export default DataMarker;